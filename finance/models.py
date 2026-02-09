from django.db import models
from django.conf import settings


class Service(models.Model):
    """مدل خدمات"""
    name = models.CharField(max_length=100, verbose_name="نام خدمت")
    price = models.DecimalField(max_digits=12, decimal_places=0, verbose_name="قیمت (ریال)")

    class Meta:
        verbose_name = "خدمت"
        verbose_name_plural = "خدمات"

    def __str__(self):
        return self.name


class Transaction(models.Model):
    """مدل تراکنش"""
    STATUS_CHOICES = [
        ('paid', 'پرداخت شده'),
        ('pending', 'در انتظار'),
        ('failed', 'ناموفق')
    ]

    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='transactions', verbose_name="بیمار")
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, verbose_name="خدمت")
    amount = models.DecimalField(max_digits=12, decimal_places=0, verbose_name="مبلغ")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name="وضعیت")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    class Meta:
        verbose_name = "تراکنش"
        verbose_name_plural = "تراکنش‌ها"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.patient.phone_number} - {self.amount}"