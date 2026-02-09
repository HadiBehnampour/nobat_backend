from django.contrib import admin
from .models import Transaction, Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name',)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('patient', 'service', 'amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('patient__phone_number', 'service__name')
    readonly_fields = ('created_at',)