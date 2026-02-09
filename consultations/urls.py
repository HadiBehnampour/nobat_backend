from django.urls import path
from .views import (
    ConsultationAPIView,
    ConsultationDetailAPIView,
    ConsultationAnswerAPIView,
)

app_name = 'consultations'

urlpatterns = [
    path('chat/', ConsultationAPIView.as_view(), name='consultation_list'),
    path('chat/<int:pk>/', ConsultationDetailAPIView.as_view(), name='consultation_detail'),
    path('chat/<int:pk>/answer/', ConsultationAnswerAPIView.as_view(), name='consultation_answer'),
]