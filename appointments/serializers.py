from rest_framework import serializers
from .models import TimeSlot, Appointment
import jdatetime


class TimeSlotSerializer(serializers.ModelSerializer):
    """سریالایزر اسلات زمانی"""
    is_available = serializers.SerializerMethodField()
    jalali_date = serializers.SerializerMethodField()
    jalali_date_formatted = serializers.SerializerMethodField()

    class Meta:
        model = TimeSlot
        fields = [
            'id', 'date', 'jalali_date', 'jalali_date_formatted',
            'start_time', 'is_blocked', 'is_available', 'created_at'
        ]
        read_only_fields = ['created_at']

    def get_is_available(self, obj):
        return obj.is_available

    def get_jalali_date(self, obj):
        return obj.get_jalali_date()

    def get_jalali_date_formatted(self, obj):
        return obj.get_jalali_date_formatted()


class AppointmentSerializer(serializers.ModelSerializer):
    """سریالایزر نوبت ویزیت"""

    slot_detail = TimeSlotSerializer(source='slot', read_only=True)
    patient_phone = serializers.SerializerMethodField()
    patient_name = serializers.SerializerMethodField()
    patient_national_id = serializers.SerializerMethodField()
    patient_birth_date = serializers.SerializerMethodField()
    patient_insurance_type = serializers.SerializerMethodField()
    patient_insurance_code = serializers.SerializerMethodField()
    patient_supplementary = serializers.SerializerMethodField()
    patient_address = serializers.SerializerMethodField()
    patient_medical_history = serializers.SerializerMethodField()
    patient_blood_group = serializers.SerializerMethodField()
    patient_profile_complete = serializers.SerializerMethodField()

    day_of_week = serializers.CharField(read_only=True)
    display_date = serializers.CharField(read_only=True)
    display_date_formatted = serializers.CharField(read_only=True)
    display_time = serializers.CharField(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    type_display = serializers.CharField(source='get_booking_type_display', read_only=True)
    source_display = serializers.CharField(source='get_source_display', read_only=True)

    class Meta:
        model = Appointment
        fields = [
            'id', 'patient', 'patient_phone', 'patient_name', 'patient_national_id',
            'patient_birth_date', 'patient_insurance_type', 'patient_insurance_code',
            'patient_supplementary', 'patient_address', 'patient_medical_history',
            'patient_blood_group', 'patient_profile_complete', 'slot', 'slot_detail',
            'source', 'source_display', 'status', 'status_display',
            'booking_type', 'type_display', 'is_paid', 'price', 'visit_reason', 'notes',
            'day_of_week', 'display_date', 'display_date_formatted', 'display_time',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_patient_phone(self, obj):
        if obj.patient:
            return obj.patient.phone_number
        return None

    def get_patient_name(self, obj):
        if obj.patient:
            name = obj.patient.get_full_name()
            return name if name else obj.patient.phone_number
        return "بدون بیمار"

    def get_patient_national_id(self, obj):
        if obj.patient and hasattr(obj.patient, 'patient_profile'):
            return obj.patient.patient_profile.national_code
        return None

    def get_patient_birth_date(self, obj):
        if obj.patient and hasattr(obj.patient, 'patient_profile'):
            birth_date = obj.patient.patient_profile.birth_date
            if birth_date:
                try:
                    j_date = jdatetime.date.fromgregorian(date=birth_date)
                    return str(j_date)
                except Exception:
                    return None
        return None

    def get_patient_insurance_type(self, obj):
        if obj.patient and hasattr(obj.patient, 'patient_profile'):
            return obj.patient.patient_profile.get_insurance_type_display()
        return "نامعلوم"

    def get_patient_insurance_code(self, obj):
        if obj.patient and hasattr(obj.patient, 'patient_profile'):
            return obj.patient.patient_profile.insurance_code
        return None

    def get_patient_supplementary(self, obj):
        if obj.patient and hasattr(obj.patient, 'patient_profile'):
            return obj.patient.patient_profile.get_supplementary_display()
        return "ندارد"

    def get_patient_address(self, obj):
        if obj.patient and hasattr(obj.patient, 'patient_profile'):
            return obj.patient.patient_profile.full_address
        return None

    def get_patient_medical_history(self, obj):
        if obj.patient and hasattr(obj.patient, 'patient_profile'):
            return obj.patient.patient_profile.medical_history
        return None

    def get_patient_blood_group(self, obj):
        if obj.patient and hasattr(obj.patient, 'patient_profile'):
            return obj.patient.patient_profile.blood_group
        return None

    def get_patient_profile_complete(self, obj):
        if obj.patient and hasattr(obj.patient, 'patient_profile'):
            return obj.patient.patient_profile.profile_complete
        return False