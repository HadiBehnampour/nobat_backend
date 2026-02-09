from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from .models import Consultation
from .serializers import ConsultationSerializer


class ConsultationAPIView(APIView):
    """لیست و ارسال مشاوره"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.is_doctor or request.user.is_secretary:
            consults = Consultation.objects.all().order_by('-created_at')
        else:
            consults = Consultation.objects.filter(patient=request.user).order_by('-created_at')

        serializer = ConsultationSerializer(consults, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data.copy()
        data['patient'] = request.user.id

        serializer = ConsultationSerializer(data=data)
        if serializer.is_valid():
            serializer.save(patient=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConsultationDetailAPIView(APIView):
    """جزئیات مشاوره"""
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        consult = get_object_or_404(Consultation, pk=pk)
        serializer = ConsultationSerializer(consult)
        return Response(serializer.data)


class ConsultationAnswerAPIView(APIView):
    """پاسخ دادن به مشاوره"""
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        consult = get_object_or_404(Consultation, pk=pk)
        answer = request.data.get('answer_text')

        if not answer:
            return Response(
                {"error": "متن پاسخ نمی‌تواند خالی باشد"},
                status=status.HTTP_400_BAD_REQUEST
            )

        consult.answer_text = answer
        consult.status = 'answered'
        consult.answered_at = now()
        consult.save()

        serializer = ConsultationSerializer(consult)
        return Response({
            "message": "✅ پاسخ ثبت شد",
            "consultation": serializer.data
        })