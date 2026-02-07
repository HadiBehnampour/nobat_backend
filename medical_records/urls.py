from django.urls import path
from .views import PatientHistoryAPIView, CreateRecordAPIView

urlpatterns = [
    # آدرس برای دریافت تاریخچه (مثال: /api/medical/history/5/)
    path('history/<int:patient_id>/', PatientHistoryAPIView.as_view(), name='patient_history'),
    # آدرس برای ثبت ویزیت جدید
    path('create/', CreateRecordAPIView.as_view(), name='create_record'),
]