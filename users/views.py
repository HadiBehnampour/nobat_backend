from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import User, PatientProfile
from .serializers import UserSerializer, PatientProfileSerializer


class OTPRequestAPIView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        if not phone_number:
            return Response({"error": "شماره موبایل الزامی است"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "کد تایید ارسال شد", "test_code": "1234"}, status=status.HTTP_200_OK)


class OTPVerifyAPIView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        code = request.data.get('code')

        if code == "1234":
            # هماهنگ با مدل شما (بدون username)
            user, created = User.objects.get_or_create(phone_number=phone_number)
            if created:
                user.is_patient = True
                user.save()
                PatientProfile.objects.get_or_create(user=user)

            serializer = UserSerializer(user)
            return Response({"message": "ورود موفق", "user": serializer.data})
        return Response({"error": "کد اشتباه است"}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileAPIView(APIView):
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PatientProfileDetailAPIView(APIView):
    """تکمیل اطلاعات پروفایل (کد ملی و...)"""

    def get(self, request):
        profile = get_object_or_404(PatientProfile, user=request.user)
        serializer = PatientProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request):
        profile = get_object_or_404(PatientProfile, user=request.user)
        serializer = PatientProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)