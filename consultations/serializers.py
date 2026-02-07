from rest_framework import serializers
from .models import Consultation

class ConsultationSerializer(serializers.ModelSerializer):
    patient_phone = serializers.ReadOnlyField(source='patient.phone_number')
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Consultation
        fields = [
            'id', 'patient', 'patient_phone', 'subject',
            'question_text', 'answer_text', 'status',
            'status_display', 'created_at', 'answered_at'
        ]
        read_only_fields = ['status', 'created_at', 'answered_at']