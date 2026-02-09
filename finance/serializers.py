from rest_framework import serializers
from .models import Transaction, Service


class ServiceSerializer(serializers.ModelSerializer):
    """سریالایزر خدمت"""
    class Meta:
        model = Service
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
    """سریالایزر تراکنش"""
    patient_phone = serializers.ReadOnlyField(source='patient.phone_number')
    service_name = serializers.ReadOnlyField(source='service.name')

    class Meta:
        model = Transaction
        fields = [
            'id', 'patient', 'patient_phone', 'service', 'service_name',
            'amount', 'status', 'created_at'
        ]