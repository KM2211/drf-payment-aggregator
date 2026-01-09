from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action

from .models import Payment
from .serializers import PaymentCreateSerializer, PaymentReadSerializer
from merchants.permissions import IsAuthenticatedMerchant
from ledger.models import LedgerEntry
from payments.state_machine import can_transition, PaymentStates
from payments.gateways.registry import get_gateway


class PaymentViewSet(ModelViewSet):
    """
    DRF ModelViewSet
    Supports:
    - create
    - retrieve
    """

    permission_classes = [IsAuthenticatedMerchant]
    http_method_names = ["post", "get"]

    def get_queryset(self):
        return Payment.objects.filter(merchant=self.request.user)

    def get_serializer_class(self):
        if self.action == "create":
            return PaymentCreateSerializer
        return PaymentReadSerializer

    def create(self, request, *args, **kwargs):
        idem_key = request.headers.get("Idempotency-Key")
        if not idem_key:
            raise ValidationError("Idempotency-Key header is required")

        existing = Payment.objects.filter(
            merchant=request.user,
            idempotency_key=idem_key
        ).first()

        if existing:
            serializer = PaymentReadSerializer(existing)
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        payment = Payment.objects.create(
            merchant=request.user,
            amount=serializer.validated_data["amount"],
            currency=serializer.validated_data["currency"],
            idempotency_key=idem_key,
            gateway="mock_success",
            status=PaymentStates.CREATED,
        )

        from payments.tasks import process_payment
        process_payment.delay(payment.id)

        read_serializer = PaymentReadSerializer(payment)
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)


    @action(detail=True, methods=["post"])
    def refund(self, request, pk=None):
        payment = self.get_object()

        if not can_transition(payment.status, PaymentStates.REFUNDED):
            return Response(
                {"error": "Invalid state transition"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        payment.status = PaymentStates.REFUNDED
        payment.save(update_fields=["status"])

        LedgerEntry.objects.create(
            payment=payment,
            event="REFUND",
            amount=-payment.amount,
        )

        serializer = PaymentReadSerializer(payment)
        return Response(serializer.data, status=status.HTTP_200_OK)
