from django.urls import path
from .views import (
    DoctorProfileAPIView,
    OfficeSettingsAPIView,
    WorkingHoursAPIView,
    WorkingHourDetailAPIView,
)

app_name = 'settings_config'

urlpatterns = [
    path('doctor/', DoctorProfileAPIView.as_view(), name='doctor_profile'),
    path('office/', OfficeSettingsAPIView.as_view(), name='office_settings'),
    path('hours/', WorkingHoursAPIView.as_view(), name='working_hours'),
    path('hours/<int:day>/', WorkingHourDetailAPIView.as_view(), name='working_hour_detail'),
]