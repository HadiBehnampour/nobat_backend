from django.urls import path
from .views import OTPRequestAPIView, OTPVerifyAPIView, UserProfileAPIView, PatientProfileDetailAPIView

urlpatterns = [
    path('auth/otp-request/', OTPRequestAPIView.as_view(), name='otp_request'),
    path('auth/verify/', OTPVerifyAPIView.as_view(), name='otp_verify'),
    path('profile/', UserProfileAPIView.as_view(), name='user_profile'),
    path('profile/patient/', PatientProfileDetailAPIView.as_view(), name='patient_profile'),
]