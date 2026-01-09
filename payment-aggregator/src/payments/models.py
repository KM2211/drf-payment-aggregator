from django.db import models
from merchants.models import Merchant
import uuid

class Payment(models.Model):
    STATUS_CREATED = "CREATED"
    STATUS_PROCESSING = "PROCESSING"
    STATUS_SUCCESS = "SUCCESS"
    STATUS_FAILED = "FAILED"
    STATUS_REFUNDED = "REFUNDED"

    STATUS_CHOICES = [
        (STATUS_CREATED, "CREATED"),
        (STATUS_PROCESSING, "PROCESSING"),
        (STATUS_SUCCESS, "SUCCESS"),
        (STATUS_FAILED, "FAILED"),
        (STATUS_REFUNDED, "REFUNDED"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    merchant = models.ForeignKey(Merchant, on_delete=models.PROTECT)

    amount = models.PositiveBigIntegerField()
    currency = models.CharField(max_length=10)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_CREATED,
    )
    idempotency_key = models.CharField(max_length=128)
    gateway = models.CharField(max_length=50, default="mock_success")


    created_at = models.DateTimeField(auto_now_add=True)
    
    # class Meta:
    #     unique_together = ("merchant", "idempotency_key")

