from django.db import models
from django.conf import settings


class Service(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام خدمت")
    price = models.DecimalField(max_digits=12, decimal_places=0, verbose_name="قیمت (ریال)")

    def __str__(self):
        return self.name


class Transaction(models.Model):
    STATUS_CHOICES = [('paid', 'پرداخت شده'), ('pending', 'در انتظار'), ('failed', 'ناموفق')]

    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='transactions')
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.phone_number} - {self.amount}"