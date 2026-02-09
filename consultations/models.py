from django.db import models
from django.conf import settings


class Consultation(models.Model):
    """مدل مشاوره"""
    STATUS_CHOICES = [
        ('pending', 'در انتظار پاسخ'),
        ('answered', 'پاسخ داده شده')
    ]

    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='questions', verbose_name="بیمار")
    subject = models.CharField(max_length=200, verbose_name="موضوع")
    question_text = models.TextField(verbose_name="متن سوال")
    answer_text = models.TextField(null=True, blank=True, verbose_name="پاسخ پزشک")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name="وضعیت")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    answered_at = models.DateTimeField(null=True, blank=True, verbose_name="تاریخ پاسخ")

    class Meta:
        verbose_name = "مشاوره"
        verbose_name_plural = "مشاوره‌ها"
        ordering = ['-created_at']

    def __str__(self):
        return f"سوال {self.patient.phone_number} - {self.subject}"