import pandas as pd
import io
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Transaction, Service
from .serializers import TransactionSerializer, ServiceSerializer


class TransactionListAPIView(APIView):
    """لیست تمام تراکنش‌ها برای پنل مدیریت"""

    def get(self, request):
        transactions = Transaction.objects.all().order_by('-created_at')
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)


class FinanceExcelExportAPIView(APIView):
    """خروجی اکسل بدون ارور بصری"""

    def get(self, request):
        data = Transaction.objects.all().values(
            'patient__phone_number', 'service__name', 'amount', 'status', 'created_at'
        )
        df = pd.DataFrame(list(data))

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)

        response = HttpResponse(
            output.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="report.xlsx"'
        return response


class ServiceManagerAPIView(APIView):
    """مدیریت تعرفه خدمات"""

    def get(self, request):
        services = Service.objects.all()
        return Response(ServiceSerializer(services, many=True).data)

    def post(self, request):
        serializer = ServiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)