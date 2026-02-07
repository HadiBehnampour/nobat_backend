from django.db import models
from django.conf import settings

class TimeSlot(models.Model):
    date = models.DateField()
    start_time = models.TimeField()
    is_blocked = models.BooleanField(default=False, verbose_name="بسته شده")

    def __str__(self):
        return f"{self.date} - {self.start_time}"

class Appointment(models.Model):
    SOURCE_CHOICES = [('site', 'سایت'), ('manual', 'دستی'), ('scraper', 'خارجی')]
    STATUS_CHOICES = [('reserved', 'رزرو'), ('waiting', 'اتاق انتظار'), ('completed', 'پایان ویزیت')]
    TYPE_CHOICES = [('in_person', 'حضوری'), ('phone', 'تلفنی')]

    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    slot = models.OneToOneField(TimeSlot, on_delete=models.CASCADE, related_name='appointment')
    source = models.CharField(max_length=10, choices=SOURCE_CHOICES, default='site')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='reserved')
    booking_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='in_person')
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"نوبت {self.id} - {self.status}"