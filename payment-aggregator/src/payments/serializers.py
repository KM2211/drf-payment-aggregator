from rest_framework import serializers
from .models import Payment

class PaymentCreateSerializer(serializers.Serializer):
    amount = serializers.IntegerField(min_value=1)
    currency = serializers.CharField(max_length=10)

class PaymentReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
