from django.urls import path
from .views import (
    OTPRequestAPIView,
    OTPVerifyAPIView,
    UserProfileAPIView,
    PatientProfileDetailAPIView,
    AdminPatientListAPIView,
    AdminPatientDetailAPIView,
    AdminUserListAPIView,
)

app_name = 'users'

urlpatterns = [
    # Authentication
    path('auth/otp-request/', OTPRequestAPIView.as_view(), name='otp_request'),
    path('auth/verify/', OTPVerifyAPIView.as_view(), name='otp_verify'),

    # User Profile
    path('profile/', UserProfileAPIView.as_view(), name='user_profile'),
    path('profile/patient/', PatientProfileDetailAPIView.as_view(), name='patient_profile'),

    # Admin APIs
    path('admin/patients/', AdminPatientListAPIView.as_view(), name='admin_patients_list'),
    path('admin/patients/<int:patient_id>/', AdminPatientDetailAPIView.as_view(), name='admin_patient_detail'),
    path('admin/users/', AdminUserListAPIView.as_view(), name='admin_users_list'),
]