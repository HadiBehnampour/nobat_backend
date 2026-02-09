from rest_framework import serializers
from .models import Consultation


class ConsultationSerializer(serializers.ModelSerializer):
    """سریالایزر مشاوره"""
    patient_phone = serializers.ReadOnlyField(source='patient.phone_number')
    patient_name = serializers.SerializerMethodField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Consultation
        fields = [
            'id', 'patient', 'patient_phone', 'patient_name', 'subject',
            'question_text', 'answer_text', 'status', 'status_display',
            'created_at', 'answered_at'
        ]
        read_only_fields = ['created_at', 'answered_at']

    def get_patient_name(self, obj):
        name = obj.patient.get_full_name()
        return name if name else obj.patient.phone_number