from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import DoctorProfile, OfficeSettings, WorkingHour
from .serializers import DoctorProfileSerializer, OfficeSettingsSerializer, WorkingHourSerializer


class DoctorProfileAPIView(APIView):
    """دریافت پروفایل پزشک"""

    def get(self, request):
        doctor = DoctorProfile.objects.first()
        if not doctor:
            return Response(
                {"error": "پروفایل پزشک یافت نشد"},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = DoctorProfileSerializer(doctor)
        return Response(serializer.data)

    def put(self, request):
        doctor = DoctorProfile.objects.first()
        if not doctor:
            serializer = DoctorProfileSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            serializer = DoctorProfileSerializer(doctor, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OfficeSettingsAPIView(APIView):
    """مدیریت تنظیمات مطب"""

    def get(self, request):
        settings, _ = OfficeSettings.objects.get_or_create(id=1)
        serializer = OfficeSettingsSerializer(settings)
        return Response(serializer.data)

    def put(self, request):
        settings, _ = OfficeSettings.objects.get_or_create(id=1)
        serializer = OfficeSettingsSerializer(settings, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WorkingHoursAPIView(APIView):
    """مدیریت ساعات کاری"""

    def get(self, request):
        hours = WorkingHour.objects.all().order_by('day')
        serializer = WorkingHourSerializer(hours, many=True)
        return Response(serializer.data)

    def post(self, request):
        day = request.data.get('day')
        instance = WorkingHour.objects.filter(day=day).first()

        serializer = WorkingHourSerializer(
            instance,
            data=request.data
        ) if instance else WorkingHourSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED if not instance else status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WorkingHourDetailAPIView(APIView):
    """تفاصیل ساعات کاری برای روز خاص"""

    def get(self, request, day):
        hour = get_object_or_404(WorkingHour, day=day)
        serializer = WorkingHourSerializer(hour)
        return Response(serializer.data)

    def put(self, request, day):
        hour = get_object_or_404(WorkingHour, day=day)
        serializer = WorkingHourSerializer(hour, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)