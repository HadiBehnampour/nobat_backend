from django.urls import path
from .views import ConsultationAPIView, ConsultationAnswerAPIView

urlpatterns = [
    path('chat/', ConsultationAPIView.as_view(), name='consultation_list'),
    path('chat/<int:pk>/answer/', ConsultationAnswerAPIView.as_view(), name='consultation_answer'),
]