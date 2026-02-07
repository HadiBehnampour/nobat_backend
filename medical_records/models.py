from django.db import models
from django.conf import settings


class MedicalRecord(models.Model):
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='medical_records')
    doctor_notes = models.TextField(verbose_name="یادداشت پزشک")
    prescription = models.TextField(verbose_name="نسخه", null=True, blank=True)

    # فیلدهای مربوط به BMI
    weight = models.FloatField(verbose_name="وزن (کیلوگرم)")
    height = models.FloatField(verbose_name="قد (سانتی‌متر)")
    bmi = models.FloatField(null=True, blank=True, verbose_name="شاخص توده بدنی")

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # محاسبه BMI قبل از ذخیره در دیتابیس
        # فرمول: وزن تقسیم بر (قد به توان دو) - قد به متر تبدیل می‌شود
        if self.weight and self.height:
            height_in_meters = self.height / 100
            self.bmi = round(self.weight / (height_in_meters ** 2), 2)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"ویزیت {self.patient.phone_number} - {self.created_at.date()}"