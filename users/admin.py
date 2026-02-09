from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, PatientProfile


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('phone_number', 'get_full_name', 'is_patient', 'is_doctor', 'is_secretary')
    list_filter = ('is_patient', 'is_doctor', 'is_secretary')
    search_fields = ('phone_number', 'first_name', 'last_name')
    ordering = ('phone_number',)

    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Roles', {'fields': ('is_patient', 'is_doctor', 'is_secretary')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )


@admin.register(PatientProfile)
class PatientProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'national_code', 'insurance_type', 'profile_complete')
    list_filter = ('insurance_type', 'supplementary', 'profile_complete')
    search_fields = ('user__phone_number', 'national_code')
    readonly_fields = ('created_at', 'updated_at')