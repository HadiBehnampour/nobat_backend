from django.urls import path
from .views import TransactionListAPIView, FinanceExcelExportAPIView, ServiceManagerAPIView

urlpatterns = [
    path('transactions/', TransactionListAPIView.as_view(), name='transactions'),
    path('export/', FinanceExcelExportAPIView.as_view(), name='finance_export'),
    path('services/', ServiceManagerAPIView.as_view(), name='service_manager'),
]