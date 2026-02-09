from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import MedicalRecord
from .serializers import MedicalRecordSerializer


class PatientHistoryAPIView(APIView):
    """سابقه پزشکی بیمار"""

    def get(self, request, patient_id):
        records = MedicalRecord.objects.filter(patient_id=patient_id).order_by('-created_at')
        serializer = MedicalRecordSerializer(records, many=True)
        return Response(serializer.data)


class CreateRecordAPIView(APIView):
    """ثبت رکورد پزشکی جدید"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = MedicalRecordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PatientMyHistoryAPIView(APIView):
    """سابقه پزشکی خود بیمار"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        records = MedicalRecord.objects.filter(patient=request.user).order_by('-created_at')
        serializer = MedicalRecordSerializer(records, many=True)
        return Response(serializer.data)