from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            'id',
            'user',
            'project',
            'amount',
            'method',
            'status',
            'transaction_id',
            'created_at',
        ]
        read_only_fields = ['id', 'user', 'created_at']
