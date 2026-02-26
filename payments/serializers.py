from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.Serializer):
    """Serializer for payment requests."""
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)


class PaymentResponseSerializer(serializers.ModelSerializer):
    """Serializer for payment responses."""
    
    class Meta:
        model = Payment
        fields = ['id', 'amount', 'status', 'created_at']
        read_only_fields = fields
