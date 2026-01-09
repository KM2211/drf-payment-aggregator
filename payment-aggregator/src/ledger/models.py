from django.db import models
from payments.models import Payment

class LedgerEntry(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.PROTECT)
    event = models.CharField(max_length=50)
    amount = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
