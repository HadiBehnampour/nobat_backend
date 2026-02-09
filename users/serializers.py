from rest_framework import serializers
from .models import User, PatientProfile


class PatientProfileSerializer(serializers.ModelSerializer):
    """سریالایزر پروفایل بیمار"""
    insurance_type_display = serializers.CharField(source='get_insurance_type_display', read_only=True)
    supplementary_display = serializers.CharField(source='get_supplementary_display', read_only=True)

    class Meta:
        model = PatientProfile
        fields = [
            'id', 'national_code', 'birth_date', 'blood_group', 'full_address',
            'insurance_type', 'insurance_type_display', 'insurance_code',
            'supplementary', 'supplementary_display', 'medical_history',
            'allergies', 'current_medications', 'profile_complete',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class UserSerializer(serializers.ModelSerializer):
    """سریالایزر کاربر"""
    patient_profile = PatientProfileSerializer(source='patient_profile', read_only=True)
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'phone_number', 'first_name', 'last_name', 'full_name',
            'email', 'is_patient', 'is_doctor', 'is_secretary',
            'patient_profile', 'date_joined'
        ]
        read_only_fields = ['id', 'date_joined']

    def get_full_name(self, obj):
        return obj.get_full_name()


class UserDetailSerializer(serializers.ModelSerializer):
    """سریالایزر کاربر با جزئیات"""
    patient_profile = PatientProfileSerializer(read_only=True)
    full_name = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'phone_number', 'first_name', 'last_name', 'full_name',
            'email', 'is_patient', 'is_doctor', 'is_secretary', 'role',
            'patient_profile', 'date_joined'
        ]
        read_only_fields = ['id', 'date_joined']

    def get_full_name(self, obj):
        return obj.get_full_name()

    def get_role(self, obj):
        if obj.is_doctor:
            return 'doctor'
        elif obj.is_secretary:
            return 'secretary'
        elif obj.is_patient:
            return 'patient'
        return 'user'