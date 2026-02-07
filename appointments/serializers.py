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
        fields = ['id', 'patient', 'slot', 'source', 'status', 'booking_type', 'is_paid', 'visit_reason']
        
        
from jalali_date import date2jalali

class TimeSlotSerializer(serializers.ModelSerializer):
    jalali_date = serializers.SerializerMethodField()

    class Meta:
        model = TimeSlot
        fields = ['id', 'date', 'jalali_date', 'start_time', 'is_blocked']

    def get_jalali_date(self, obj):
        return date2jalali(obj.date).strftime('%Y/%m/%d')