from celery import shared_task
from payments.models import Payment
from ledger.models import LedgerEntry
from payments.gateways.registry import get_gateway
from payments.state_machine import can_transition, PaymentStates


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=5)
def process_payment(self, payment_id):
    payment = Payment.objects.get(id=payment_id)

    # move to PROCESSING
    if not can_transition(payment.status, PaymentStates.PROCESSING):
        return

    payment.status = PaymentStates.PROCESSING
    payment.save(update_fields=["status"])

    gateway = get_gateway(payment.gateway)
    result = gateway.charge(payment)

    if can_transition(payment.status, result["status"]):
        payment.status = result["status"]
        payment.save(update_fields=["status"])

        LedgerEntry.objects.create(
            payment=payment,
            event="CHARGE",
            amount=payment.amount if payment.status == PaymentStates.SUCCESS else 0,
        )
