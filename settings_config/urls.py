from django.urls import path
from .views import OfficeSettingsAPIView, WorkingHoursAPIView

urlpatterns = [
    path('office/', OfficeSettingsAPIView.as_view(), name='office_settings'),
    path('hours/', WorkingHoursAPIView.as_view(), name='working_hours'),
]