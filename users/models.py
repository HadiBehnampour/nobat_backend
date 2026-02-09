from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('شماره موبایل اجباری است')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(phone_number, password, **extra_fields)


class User(AbstractUser):
    """مدل کاربر"""
    username = None
    phone_number = models.CharField(max_length=11, unique=True, verbose_name="شماره موبایل")
    is_patient = models.BooleanField(default=False, verbose_name="بیمار")
    is_doctor = models.BooleanField(default=False, verbose_name="پزشک")
    is_secretary = models.BooleanField(default=False, verbose_name="منشی")

    objects = UserManager()
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"

    def __str__(self):
        return f"{self.get_full_name() or self.phone_number}"


class PatientProfile(models.Model):
    """پروفایل بیمار"""

    INSURANCE_TYPE_CHOICES = [
        ('none', 'بدون بیمه'),
        ('tamin', 'تامین اجتماعی'),
        ('salamat', 'سلامت'),
        ('armed', 'نیروهای مسلح'),
        ('other', 'سایر'),
    ]

    SUPPLEMENTARY_CHOICES = [
        ('none', 'ندارد'),
        ('dana', 'دنا'),
        ('asia', 'آسیا'),
        ('other', 'سایر'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile', verbose_name="کاربر")
    national_code = models.CharField(max_length=10, unique=True, null=True, blank=True, verbose_name="کد ملی")
    birth_date = models.DateField(null=True, blank=True, verbose_name="تاریخ تولد")
    blood_group = models.CharField(max_length=5, null=True, blank=True,
                                   choices=[('O+', 'O+'), ('O-', 'O-'), ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'),
                                            ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-')], verbose_name="گروه خونی")
    full_address = models.TextField(null=True, blank=True, verbose_name="آدرس کامل")
    insurance_type = models.CharField(max_length=20, choices=INSURANCE_TYPE_CHOICES, default='none',
                                      verbose_name="نوع بیمه")
    insurance_code = models.CharField(max_length=20, null=True, blank=True, verbose_name="شماره بیمه")
    supplementary = models.CharField(max_length=20, choices=SUPPLEMENTARY_CHOICES, default='none',
                                     verbose_name="بیمه تکمیلی")
    medical_history = models.TextField(null=True, blank=True, verbose_name="سابقه پزشکی")
    allergies = models.TextField(null=True, blank=True, verbose_name="حساسیت‌ها")
    current_medications = models.TextField(null=True, blank=True, verbose_name="داروهای مصرفی")
    profile_complete = models.BooleanField(default=False, verbose_name="پروفایل تکمیل شده")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="آخرین بروزرسانی")

    class Meta:
        verbose_name = "پروفایل بیمار"
        verbose_name_plural = "پروفایل‌های بیماران"

    def __str__(self):
        return f"پروفایل {self.user.get_full_name() or self.user.phone_number}"

    def mark_as_complete(self):
        if all([self.national_code, self.birth_date, self.full_address, self.insurance_type != 'none']):
            self.profile_complete = True
            self.save()
            return True
        return False