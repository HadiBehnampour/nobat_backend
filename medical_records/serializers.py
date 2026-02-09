from rest_framework import serializers
from .models import MedicalRecord


class MedicalRecordSerializer(serializers.ModelSerializer):
    """سریالایزر رکورد پزشکی"""
    patient_name = serializers.SerializerMethodField()

    class Meta:
        model = MedicalRecord
        fields = [
            'id', 'patient', 'patient_name', 'doctor_notes', 'prescription',
            'weight', 'height', 'bmi', 'created_at'
        ]
        read_only_fields = ['bmi', 'created_at']

    def get_patient_name(self, obj):
        name = obj.patient.get_full_name()
        return name if name else obj.patient.phone_number