from django.urls import path
from .views import (
    TransactionListAPIView,
    TransactionDetailAPIView,
    ServiceListAPIView,
    FinanceStatsAPIView,
)

app_name = 'finance'

urlpatterns = [
    path('transactions/', TransactionListAPIView.as_view(), name='transaction_list'),
    path('transactions/<int:pk>/', TransactionDetailAPIView.as_view(), name='transaction_detail'),
    path('services/', ServiceListAPIView.as_view(), name='service_list'),
    path('stats/', FinanceStatsAPIView.as_view(), name='finance_stats'),
]