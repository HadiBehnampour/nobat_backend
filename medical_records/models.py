from django.db import models
from django.conf import settings


class MedicalRecord(models.Model):
    """مدل رکورد پزشکی"""
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='medical_records', verbose_name="بیمار")
    doctor_notes = models.TextField(verbose_name="یادداشت پزشک")
    prescription = models.TextField(verbose_name="نسخه", null=True, blank=True)
    weight = models.FloatField(verbose_name="وزن (کیلوگرم)")
    height = models.FloatField(verbose_name="قد (سانتی‌متر)")
    bmi = models.FloatField(null=True, blank=True, verbose_name="شاخص توده بدنی")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    class Meta:
        verbose_name = "رکورد پزشکی"
        verbose_name_plural = "رکوردهای پزشکی"
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if self.weight and self.height:
            height_in_meters = self.height / 100
            self.bmi = round(self.weight / (height_in_meters ** 2), 2)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"ویزیت {self.patient.phone_number} - {self.created_at.date()}"