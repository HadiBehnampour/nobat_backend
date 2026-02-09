from django.contrib import admin
from .models import TimeSlot, Appointment


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('get_jalali_date', 'start_time', 'is_blocked', 'is_available')
    list_filter = ('is_blocked', 'date')
    search_fields = ('jalali_date_cached',)
    readonly_fields = ('jalali_date_cached', 'get_jalali_date_formatted')

    def get_jalali_date(self, obj):
        return obj.get_jalali_date()

    get_jalali_date.short_description = "تاریخ شمسی"


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'get_date', 'get_time', 'status', 'source', 'is_paid')
    list_filter = ('status', 'source', 'booking_type', 'is_paid')
    search_fields = ('patient__phone_number', 'patient__first_name')
    readonly_fields = ('created_at', 'updated_at', 'display_date', 'display_date_formatted')

    def get_date(self, obj):
        return obj.display_date

    get_date.short_description = "تاریخ"

    def get_time(self, obj):
        return obj.display_time

    get_time.short_description = "ساعت"