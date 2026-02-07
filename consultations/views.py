from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from .models import Consultation
from .serializers import ConsultationSerializer


class ConsultationAPIView(APIView):
    """ارسال سوال توسط بیمار و نمایش لیست"""

    def get(self, request):
        if not request.user.is_authenticated:
            return Response({"error": "لطفا وارد شوید"}, status=status.HTTP_401_UNAUTHORIZED)

        # پزشک همه را می‌بیند، بیمار فقط سوالات خودش
        if request.user.is_doctor or request.user.is_secretary:
            consults = Consultation.objects.all().order_by('-created_at')
        else:
            consults = Consultation.objects.filter(patient=request.user).order_by('-created_at')

        serializer = ConsultationSerializer(consults, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ConsultationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(patient=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConsultationAnswerAPIView(APIView):
    """ثبت پاسخ توسط پزشک"""

    def patch(self, request, pk):
        consult = get_object_or_404(Consultation, pk=pk)
        answer = request.data.get('answer_text')

        if answer:
            consult.answer_text = answer
            consult.status = 'answered'
            consult.answered_at = now()
            consult.save()
            return Response({"message": "پاسخ ثبت شد"})
        return Response({"error": "متن پاسخ نمی‌تواند خالی باشد"}, status=status.HTTP_400_BAD_REQUEST)