from django.urls import path
from .views import (
    PatientHistoryAPIView,
    CreateRecordAPIView,
    PatientMyHistoryAPIView,
)

app_name = 'medical_records'

urlpatterns = [
    path('history/<int:patient_id>/', PatientHistoryAPIView.as_view(), name='patient_history'),
    path('create/', CreateRecordAPIView.as_view(), name='create_record'),
    path('my-history/', PatientMyHistoryAPIView.as_view(), name='my_history'),
]