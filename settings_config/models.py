from django.db import models


class OfficeSettings(models.Model):
    doctor_name = models.CharField(max_length=100, default="نام پزشک")
    specialty = models.CharField(max_length=100, blank=True)
    biography = models.TextField(blank=True)
    address = models.TextField(blank=True)
    phone_number = models.CharField(max_length=20, blank=True)

    # تنظیمات پیامک
    send_sms_on_book = models.BooleanField(default=True, verbose_name="پیامک هنگام رزرو")
    send_sms_reminder = models.BooleanField(default=True, verbose_name="پیامک یادآوری")

    def __str__(self):
        return f"تنظیمات مطب {self.doctor_name}"


class WorkingHour(models.Model):
    DAYS_OF_WEEK = [
        (0, 'شنبه'), (1, 'یکشنبه'), (2, 'دوشنبه'),
        (3, 'سه‌شنبه'), (4, 'چهارشنبه'), (5, 'پنج‌شنبه'), (6, 'جمعه'),
    ]
    day = models.IntegerField(choices=DAYS_OF_WEEK, unique=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.get_day_display()}: {self.start_time} - {self.end_time}"