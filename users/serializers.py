from rest_framework import serializers
from .models import User, PatientProfile

class PatientProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientProfile
        fields = ['national_code', 'blood_group', 'full_address']

class UserSerializer(serializers.ModelSerializer):
    # نمایش اطلاعات پروفایل در کنار اطلاعات کاربر
    profile = PatientProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'phone_number', 'first_name', 'last_name', 'is_patient', 'is_doctor', 'is_secretary', 'profile']