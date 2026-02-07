from rest_framework import serializers
from .models import MedicalRecord


class MedicalRecordSerializer(serializers.ModelSerializer):
    patient_name = serializers.ReadOnlyField(source='patient.get_full_name')

    class Meta:
        model = MedicalRecord
        fields = [
            'id', 'patient', 'patient_name', 'doctor_notes',
            'prescription', 'weight', 'height', 'bmi', 'created_at'
        ]
        read_only_fields = ['bmi', 'created_at']