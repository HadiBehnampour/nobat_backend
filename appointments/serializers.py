from rest_framework import serializers
from .models import TimeSlot, Appointment

class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = '__all__'

class AppointmentSerializer(serializers.ModelSerializer):
    # نمایش جزئیات اسلات در داخل نوبت
    slot_detail = TimeSlotSerializer(source='slot', read_only=True)
    patient_phone = serializers.ReadOnlyField(source='patient.phone_number')

    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'patient_phone', 'slot', 'slot_detail', 'source', 'status', 'booking_type', 'is_paid']