from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import MedicalRecord
from .serializers import MedicalRecordSerializer

class PatientHistoryAPIView(APIView):
    """مشاهده لیست تمام ویزیت‌های یک بیمار خاص (برای پزشک یا خود بیمار)"""
    def get(self, request, patient_id):
        records = MedicalRecord.objects.filter(patient_id=patient_id).order_by('-created_at')
        serializer = MedicalRecordSerializer(records, many=True)
        return Response(serializer.data)

class CreateRecordAPIView(APIView):
    """ثبت ویزیت جدید توسط پزشک"""
    def post(self, request):
        serializer = MedicalRecordSerializer(data=request.data)
        if serializer.is_valid():
            # اینجا بیمار از طریق ID فرستاده شده در ریکوئست ست می‌شود
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)