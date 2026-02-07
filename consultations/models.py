from django.db import models
from django.conf import settings


class Consultation(models.Model):
    STATUS_CHOICES = [('pending', 'در انتظار پاسخ'), ('answered', 'پاسخ داده شده')]

    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='questions')
    subject = models.CharField(max_length=200, verbose_name="موضوع")
    question_text = models.TextField(verbose_name="متن سوال")

    answer_text = models.TextField(null=True, blank=True, verbose_name="پاسخ پزشک")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    created_at = models.DateTimeField(auto_now_add=True)
    answered_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"سوال {self.patient.phone_number} - {self.subject}"