from django.db import models
from django.conf import settings
from django_jalali.db import models as jmodels


class TimeSlot(models.Model):
    # استفاده از jDateField برای ذخیره استاندارد تاریخ شمسی در دیتابیس
    date = jmodels.jDateField(verbose_name="تاریخ شمسی")
    start_time = models.TimeField(verbose_name="ساعت شروع")
    # اضافه کردن فیلد ظرفیت یا وضعیت رزرو (اختیاری اما برای فرانت مفید است)
    is_blocked = models.BooleanField(default=False, verbose_name="بسته شده")

    class Meta:
        verbose_name = "زمان حضور"
        verbose_name_plural = "زمان‌های حضور"
        # جلوگیری از ایجاد نوبت تکراری در یک زمان خاص
        unique_together = ['date', 'start_time']


    def __str__(self):
        # نمایش تاریخ شمسی در پنل ادمین
        return f"{self.date} - {self.start_time}"


class Appointment(models.Model):
    SOURCE_CHOICES = [('site', 'سایت'), ('manual', 'دستی'), ('scraper', 'خارجی')]
    STATUS_CHOICES = [('reserved', 'رزرو'), ('waiting', 'اتاق انتظار'), ('completed', 'پایان ویزیت')]
    TYPE_CHOICES = [('in_person', 'حضوری'), ('phone', 'تلفنی')]

    # فیلد علت مراجعه برای هماهنگی با visitReason در فرانت‌اِند
    visit_reason = models.TextField(null=True, blank=True, verbose_name="علت مراجعه")

    # تغییر on_delete به SET_NULL برای بیمار (اگر حساب بیمار حذف شد، نوبت باقی بماند)
    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='appointments',
        verbose_name="بیمار"
    )

    slot = models.OneToOneField(
        TimeSlot,
        on_delete=models.CASCADE,
        related_name='appointment',
        verbose_name="زمان نوبت"
    )

    source = models.CharField(max_length=10, choices=SOURCE_CHOICES, default='site', verbose_name="منبع نوبت")
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='reserved', verbose_name="وضعیت")
    booking_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='in_person', verbose_name="نوع نوبت")
    is_paid = models.BooleanField(default=False, verbose_name="پرداخت شده")

    # اضافه کردن تاریخ ثبت نوبت برای گزارش‌گیری مالی
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")

    class Meta:
        verbose_name = "نوبت"
        verbose_name_plural = "نوبت‌ها"
        ordering = ['-created_at']

    def __str__(self):
        return f"نوبت {self.id} - {self.visit_reason[:20] if self.visit_reason else 'بدون توضیح'}"