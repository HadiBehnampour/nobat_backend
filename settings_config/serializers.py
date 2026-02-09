from rest_framework import serializers
from .models import DoctorProfile, OfficeSettings, WorkingHour


class DoctorProfileSerializer(serializers.ModelSerializer):
    """سریالایزر پروفایل پزشک"""
    class Meta:
        model = DoctorProfile
        fields = [
            'id', 'doctor_name', 'specialty', 'biography', 'education',
            'experience', 'phone_number', 'email', 'profile_image',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class OfficeSettingsSerializer(serializers.ModelSerializer):
    """سریالایزر تنظیمات مطب"""
    class Meta:
        model = OfficeSettings
        fields = [
            'id', 'doctor_name', 'specialty', 'biography', 'address',
            'phone_number', 'default_interval', 'default_appointment_price',
            'send_sms_on_book', 'send_sms_reminder', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class WorkingHourSerializer(serializers.ModelSerializer):
    """سریالایزر ساعات کاری"""
    day_display = serializers.CharField(source='get_day_display', read_only=True)

    class Meta:
        model = WorkingHour
        fields = [
            'id', 'day', 'day_display', 'start_time', 'end_time',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']