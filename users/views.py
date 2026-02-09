from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import User, PatientProfile
from .serializers import UserSerializer, UserDetailSerializer, PatientProfileSerializer


class OTPRequestAPIView(APIView):
    """درخواست کد تایید"""

    def post(self, request):
        phone_number = request.data.get('phone_number')
        if not phone_number:
            return Response(
                {"error": "شماره موبایل الزامی است"},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {"message": "کد تایید ارسال شد", "test_code": "1234"},
            status=status.HTTP_200_OK
        )


class OTPVerifyAPIView(APIView):
    """تایید کد و ورود/ثبت‌نام"""

    def post(self, request):
        phone_number = request.data.get('phone_number')
        code = request.data.get('code')

        if code != "1234":
            return Response(
                {"error": "کد اشتباه است"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user, created = User.objects.get_or_create(phone_number=phone_number)

        if created:
            user.is_patient = True
            user.save()
            PatientProfile.objects.get_or_create(user=user)

        serializer = UserDetailSerializer(user)
        return Response(
            {"message": "ورود موفق", "user": serializer.data},
            status=status.HTTP_200_OK
        )


class UserProfileAPIView(APIView):
    """دریافت و بروزرسانی پروفایل کاربر"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserDetailSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserDetailSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PatientProfileDetailAPIView(APIView):
    """تکمیل و بروزرسانی پروفایل بیمار"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = get_object_or_404(PatientProfile, user=request.user)
        serializer = PatientProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request):
        profile = get_object_or_404(PatientProfile, user=request.user)
        serializer = PatientProfileSerializer(profile, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            profile.mark_as_complete()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminPatientListAPIView(APIView):
    """لیست بیماران برای ادمین"""

    def get(self, request):
        patients = PatientProfile.objects.select_related('user').all()
        serializer = PatientProfileSerializer(patients, many=True)
        return Response(serializer.data)


class AdminPatientDetailAPIView(APIView):
    """جزئیات بیمار برای ادمین"""

    def get(self, request, patient_id):
        patient = get_object_or_404(PatientProfile, user_id=patient_id)
        serializer = PatientProfileSerializer(patient)
        return Response(serializer.data)

    def put(self, request, patient_id):
        patient = get_object_or_404(PatientProfile, user_id=patient_id)
        serializer = PatientProfileSerializer(patient, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminUserListAPIView(APIView):
    """لیست کاربران برای ادمین"""

    def get(self, request):
        role = request.query_params.get('role')

        users = User.objects.all()

        if role == 'patient':
            users = users.filter(is_patient=True)
        elif role == 'doctor':
            users = users.filter(is_doctor=True)
        elif role == 'secretary':
            users = users.filter(is_secretary=True)

        serializer = UserDetailSerializer(users, many=True)
        return Response(serializer.data)