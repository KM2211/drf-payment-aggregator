from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

from payments.models import Payment
from ledger.models import LedgerEntry
from payments.state_machine import can_transition


class MockGatewayWebhook(APIView):
    authentication_classes = []  # provider → system
    permission_classes = []

    def post(self, request):
        secret = request.headers.get("X-WEBHOOK-SECRET")
        if secret != getattr(settings, "WEBHOOK_SECRET", "test_secret"):
            return Response({"error": "Invalid signature"}, status=401)

        event_id = request.data.get("event_id")
        payment_id = request.data.get("payment_id")
        outcome = request.data.get("status")  # SUCCESS / FAILED

        if not event_id or not payment_id or not outcome:
            return Response({"error": "Invalid payload"}, status=400)
        
        if outcome not in ["SUCCESS", "FAILED"]:
            return Response({"status": "ignored"}, status=200)


        # idempotency: ignore duplicate events
        if LedgerEntry.objects.filter(event=event_id).exists():
            return Response({"status": "duplicate"}, status=200)

        try:
            payment = Payment.objects.get(id=payment_id)
        except Payment.DoesNotExist:
            return Response({"error": "Payment not found"}, status=404)

        if not can_transition(payment.status, outcome):
            return Response({"status": "ignored"}, status=200)

        payment.status = outcome
        payment.save(update_fields=["status"])

        LedgerEntry.objects.create(
            payment=payment,
            event=event_id,
            amount=payment.amount if outcome == "SUCCESS" else 0,
        )
        

        return Response({"status": "processed"}, status=200)
