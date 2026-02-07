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
    username = None
    phone_number = models.CharField(max_length=11, unique=True, verbose_name="شماره موبایل")
    is_patient = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    is_secretary = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    national_code = models.CharField(max_length=10, unique=True, null=True, blank=True) # برای ثبت‌نام اولیه null باشد
    blood_group = models.CharField(max_length=5, null=True, blank=True)
    full_address = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"پروفایل {self.user.phone_number}"