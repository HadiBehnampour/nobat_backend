from django.db import models


class DoctorProfile(models.Model):
    """مدل پروفایل پزشک"""
    doctor_name = models.CharField(max_length=100, verbose_name="نام پزشک")
    specialty = models.CharField(max_length=100, verbose_name="تخصص")
    biography = models.TextField(verbose_name="بیوگرافی")
    education = models.TextField(verbose_name="تحصیلات")
    experience = models.TextField(verbose_name="تجربیات")
    phone_number = models.CharField(max_length=20, blank=True, verbose_name="شماره تلفن")
    email = models.EmailField(blank=True, verbose_name="ایمیل")
    profile_image = models.ImageField(upload_to='doctor/', null=True, blank=True, verbose_name="عکس پروفایل")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="آخرین بروزرسانی")

    class Meta:
        verbose_name = "پروفایل پزشک"
        verbose_name_plural = "پروفایل‌های پزشکان"

    def __str__(self):
        return f"{self.doctor_name} - {self.specialty}"


class OfficeSettings(models.Model):
    """مدل تنظیمات مطب"""
    doctor_name = models.CharField(max_length=100, default="نام پزشک", verbose_name="نام پزشک")
    specialty = models.CharField(max_length=100, blank=True, verbose_name="تخصص")
    biography = models.TextField(blank=True, verbose_name="بیوگرافی")
    address = models.TextField(blank=True, verbose_name="آدرس مطب")
    phone_number = models.CharField(max_length=20, blank=True, verbose_name="شماره تلفن")
    default_interval = models.IntegerField(default=30, verbose_name="فاصله پیش‌فرض نوبت‌ها (دقیقه)")
    default_appointment_price = models.IntegerField(default=0, verbose_name="قیمت پیش‌فرض نوبت (تومان)")
    send_sms_on_book = models.BooleanField(default=True, verbose_name="پیامک هنگام رزرو")
    send_sms_reminder = models.BooleanField(default=True, verbose_name="پیامک یادآوری")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="آخرین بروزرسانی")

    class Meta:
        verbose_name = "تنظیمات مطب"
        verbose_name_plural = "تنظیمات مطب"

    def __str__(self):
        return f"تنظیمات مطب {self.doctor_name}"


class WorkingHour(models.Model):
    """مدل ساعات کاری"""
    DAYS_OF_WEEK = [(0, 'شنبه'), (1, 'یکشنبه'), (2, 'دوشنبه'), (3, 'سه‌شنبه'), (4, 'چهارشنبه'), (5, 'پنج‌شنبه'),
                    (6, 'جمعه')]

    day = models.IntegerField(choices=DAYS_OF_WEEK, unique=True, verbose_name="روز هفته")
    start_time = models.TimeField(verbose_name="ساعت شروع")
    end_time = models.TimeField(verbose_name="ساعت پایان")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="آخرین بروزرسانی")

    class Meta:
        verbose_name = "ساعات کاری"
        verbose_name_plural = "ساعات کاری"
        ordering = ['day']

    def __str__(self):
        return f"{self.get_day_display()}: {self.start_time} - {self.end_time}"