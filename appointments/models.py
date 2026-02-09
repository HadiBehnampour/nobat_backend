from django.db import models
from django.conf import settings
from datetime import datetime
import jdatetime
import re


class TimeSlot(models.Model):
    """مدل اسلات زمانی"""

    date = models.DateField(verbose_name="تاریخ (میلادی)")

    jalali_date_cached = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        verbose_name="تاریخ شمسی (کش)",
        help_text="مثال: 1403/10/16"
    )

    start_time = models.TimeField(verbose_name="ساعت شروع")
    is_blocked = models.BooleanField(default=False, verbose_name="بسته شده")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date', 'start_time']
        unique_together = ['date', 'start_time']
        verbose_name = "اسلات زمانی"
        verbose_name_plural = "اسلات‌های زمانی"
        indexes = [
            models.Index(fields=['date', 'start_time']),
            models.Index(fields=['is_blocked']),
        ]

    def __str__(self):
        return f"{self.get_jalali_date()} - {self.start_time}"

    def save(self, *args, **kwargs):
        self.jalali_date_cached = self.get_jalali_date()
        super().save(*args, **kwargs)

    @property
    def is_available(self):
        return not self.is_blocked and not hasattr(self, 'appointment')

    def get_jalali_date(self):
        try:
            j_date = jdatetime.date.fromgregorian(date=self.date)
            return str(j_date)
        except Exception:
            return None

    def get_jalali_date_formatted(self):
        try:
            j_date = jdatetime.date.fromgregorian(date=self.date)
            days = {
                0: 'شنبه', 1: 'یکشنبه', 2: 'دوشنبه', 3: 'سه‌شنبه',
                4: 'چهارشنبه', 5: 'پنج‌شنبه', 6: 'جمعه',
            }
            day_name = days[self.date.weekday()]
            return f"{j_date} ({day_name})"
        except Exception:
            return None

    @staticmethod
    def convert_jalali_to_gregorian(jalali_date_str):
        """تبدیل تاریخ شمسی به میلادی"""
        if not jalali_date_str:
            return None

        try:
            normalized = str(jalali_date_str).strip()
            normalized = re.sub(r'[-.\s]', '/', normalized)

            parts = normalized.split('/')

            if len(parts) == 1 and len(normalized) == 8 and normalized.isdigit():
                parts = [normalized[0:4], normalized[4:6], normalized[6:8]]

            if len(parts) != 3:
                return None

            try:
                j_year = int(parts[0])
                j_month = int(parts[1])
                j_day = int(parts[2])
            except ValueError:
                return None

            if not (1300 <= j_year <= 1500) or not (1 <= j_month <= 12) or not (1 <= j_day <= 31):
                return None

            j_date = jdatetime.date(j_year, j_month, j_day)
            g_date = j_date.togregorian()

            return g_date

        except Exception:
            return None

    @classmethod
    def create_from_jalali(cls, jalali_date_str, start_time):
        """ایجاد TimeSlot از تاریخ شمسی"""
        gregorian_date = cls.convert_jalali_to_gregorian(jalali_date_str)

        if not gregorian_date:
            return None

        if isinstance(start_time, str):
            try:
                start_time = datetime.strptime(start_time, '%H:%M').time()
            except ValueError:
                return None

        try:
            slot, created = cls.objects.get_or_create(
                date=gregorian_date,
                start_time=start_time,
                defaults={'is_blocked': False}
            )
            return slot
        except Exception:
            return None


class Appointment(models.Model):
    """مدل نوبت ویزیت"""

    STATUS_CHOICES = [
        ('pending', 'در انتظار'),
        ('arrived', 'رسیده'),
        ('canceled', 'لغو'),
        ('completed', 'تکمیل شده'),
        ('no-show', 'عدم حضور'),
    ]

    SOURCE_CHOICES = [
        ('site', 'سایت'),
        ('manual', 'دستی'),
        ('phone', 'تلفنی'),
    ]

    TYPE_CHOICES = [
        ('in_person', 'حضوری'),
        ('phone', 'تلفنی'),
    ]

    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='appointments',
        verbose_name="بیمار"
    )
    slot = models.OneToOneField(
        TimeSlot,
        on_delete=models.CASCADE,
        related_name='appointment',
        verbose_name="اسلات زمانی"
    )

    source = models.CharField(
        max_length=10, choices=SOURCE_CHOICES, default='site', verbose_name="منبع"
    )
    status = models.CharField(
        max_length=15, choices=STATUS_CHOICES, default='pending', verbose_name="وضعیت"
    )
    booking_type = models.CharField(
        max_length=20, choices=TYPE_CHOICES, default='in_person', verbose_name="نوع ویزیت"
    )

    price = models.IntegerField(default=0, verbose_name="قیمت (تومان)")
    is_paid = models.BooleanField(default=False, verbose_name="پرداخت شده")

    visit_reason = models.TextField(null=True, blank=True, verbose_name="علت مراجعه")
    notes = models.TextField(null=True, blank=True, verbose_name="یادداشت‌های پزشک")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="آخرین بروزرسانی")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "نوبت ویزیت"
        verbose_name_plural = "نوبت‌های ویزیت"
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['patient', '-created_at']),
        ]

    def __str__(self):
        patient_name = self.patient.get_full_name() if self.patient else "بدون بیمار"
        return f"نوبت {self.id} - {patient_name} - {self.status}"

    @property
    def is_today(self):
        return self.slot.date == datetime.now().date()

    @property
    def day_of_week(self):
        days = {0: 'شنبه', 1: 'یکشنبه', 2: 'دوشنبه', 3: 'سه‌شنبه', 4: 'چهارشنبه', 5: 'پنج‌شنبه', 6: 'جمعه'}
        return days[self.slot.date.weekday()]

    @property
    def display_date(self):
        return self.slot.get_jalali_date()

    @property
    def display_date_formatted(self):
        return self.slot.get_jalali_date_formatted()

    @property
    def display_time(self):
        return self.slot.start_time.strftime('%H:%M')