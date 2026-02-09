from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Q
from .models import Transaction, Service
from .serializers import TransactionSerializer, ServiceSerializer


class TransactionListAPIView(APIView):
    """لیست تراکنش‌ها"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.is_doctor or request.user.is_secretary:
            transactions = Transaction.objects.all().order_by('-created_at')
        else:
            transactions = Transaction.objects.filter(patient=request.user).order_by('-created_at')

        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)


class TransactionDetailAPIView(APIView):
    """جزئیات تراکنش"""
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        transaction = Transaction.objects.get(pk=pk)
        if transaction.patient != request.user and not (request.user.is_doctor or request.user.is_secretary):
            return Response(
                {"error": "دسترسی غیرمجاز"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = TransactionSerializer(transaction)
        return Response(serializer.data)


class ServiceListAPIView(APIView):
    """لیست خدمات"""

    def get(self, request):
        services = Service.objects.all()
        serializer = ServiceSerializer(services, many=True)
        return Response(serializer.data)


class FinanceStatsAPIView(APIView):
    """آمار مالی"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not (request.user.is_doctor or request.user.is_secretary):
            return Response(
                {"error": "دسترسی غیرمجاز"},
                status=status.HTTP_403_FORBIDDEN
            )

        total_paid = Transaction.objects.filter(status='paid').aggregate(Sum('amount'))['amount__sum'] or 0
        total_pending = Transaction.objects.filter(status='pending').aggregate(Sum('amount'))['amount__sum'] or 0
        total_transactions = Transaction.objects.count()

        return Response({
            "total_paid": total_paid,
            "total_pending": total_pending,
            "total_transactions": total_transactions,
            "average_transaction": total_paid // max(Transaction.objects.filter(status='paid').count(), 1)
        })