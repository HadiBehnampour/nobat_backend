from django.contrib import admin
from .models import MedicalRecord


@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('patient', 'created_at', 'weight', 'height', 'bmi')
    list_filter = ('created_at',)
    search_fields = ('patient__phone_number',)
    readonly_fields = ('bmi', 'created_at')