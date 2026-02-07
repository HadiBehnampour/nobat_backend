from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import OfficeSettings, WorkingHour
from .serializers import OfficeSettingsSerializer, WorkingHourSerializer


class OfficeSettingsAPIView(APIView):
    """مدیریت اطلاعات مطب و تیک‌های پیامک"""

    def get(self, request):
        settings, _ = OfficeSettings.objects.get_or_create(id=1)
        serializer = OfficeSettingsSerializer(settings)
        return Response(serializer.data)

    def put(self, request):
        settings = get_object_or_404(OfficeSettings, id=1)
        serializer = OfficeSettingsSerializer(settings, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WorkingHoursAPIView(APIView):
    """لیست و ویرایش ساعات کاری"""

    def get(self, request):
        hours = WorkingHour.objects.all().order_by('day')
        serializer = WorkingHourSerializer(hours, many=True)
        return Response(serializer.data)

    def post(self, request):
        # اضافه کردن یا ویرایش ساعت کاری یک روز خاص
        day = request.data.get('day')
        instance = WorkingHour.objects.filter(day=day).first()
        serializer = WorkingHourSerializer(instance, data=request.data) if instance else WorkingHourSerializer(
            data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)