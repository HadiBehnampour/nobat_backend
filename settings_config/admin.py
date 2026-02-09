from django.contrib import admin
from .models import DoctorProfile, OfficeSettings, WorkingHour


@admin.register(DoctorProfile)
class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = ('doctor_name', 'specialty', 'email')
    search_fields = ('doctor_name', 'specialty')


@admin.register(OfficeSettings)
class OfficeSettingsAdmin(admin.ModelAdmin):
    list_display = ('doctor_name', 'specialty', 'default_interval')


@admin.register(WorkingHour)
class WorkingHourAdmin(admin.ModelAdmin):
    list_display = ('get_day_display', 'start_time', 'end_time', 'is_active')
    list_filter = ('is_active', 'day')