from django.contrib import admin
from .models import Consultation


@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = ('patient', 'subject', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('patient__phone_number', 'subject')
    readonly_fields = ('created_at', 'answered_at')