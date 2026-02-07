from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import TimeSlot, Appointment
from .serializers import TimeSlotSerializer, AppointmentSerializer
from datetime import datetime, timedelta


class SlotManagerAPIView(APIView):
    """تولید و نمایش اسلات‌های زمانی"""

    def get(self, request):
        date = request.query_params.get('date')
        slots = TimeSlot.objects.filter(date=date) if date else TimeSlot.objects.all()
        return Response(TimeSlotSerializer(slots, many=True).data)

    def post(self, request):
        # تولید اسلات توسط منشی (مثلا از ساعت 4 تا 8 هر 15 دقیقه)
        date = request.data.get('date')
        start = datetime.strptime(request.data.get('start_time'), '%H:%M')
        end = datetime.strptime(request.data.get('end_time'), '%H:%M')
        gap = int(request.data.get('interval', 15))

        new_slots = []
        current = start
        while current < end:
            slot, _ = TimeSlot.objects.get_or_create(date=date, start_time=current.time())
            new_slots.append(slot)
            current += timedelta(minutes=gap)
        return Response({"message": "اسلات‌ها با موفقیت ساخته شدند"}, status=status.HTTP_201_CREATED)


class AppointmentBookingAPIView(APIView):
    """رزرو نوبت جدید"""

    def post(self, request):
        slot_id = request.data.get('slot_id')
        slot = get_object_or_404(TimeSlot, id=slot_id)

        if Appointment.objects.filter(slot=slot).exists() or slot.is_blocked:
            return Response({"error": "این نوبت پر یا بسته است"}, status=status.HTTP_400_BAD_REQUEST)

        appointment = Appointment.objects.create(
            patient=request.user if request.user.is_authenticated else None,
            slot=slot,
            source=request.data.get('source', 'site'),
            booking_type=request.data.get('booking_type', 'in_person')
        )
        return Response(AppointmentSerializer(appointment).data, status=status.HTTP_201_CREATED)


class WaitingRoomAPIView(APIView):
    """مدیریت اتاق انتظار و تغییر وضعیت نوبت"""

    def get(self, request):
        # نمایش نوبت‌های امروز که در وضعیت 'waiting' یا 'reserved' هستند
        today = datetime.today().date()
        appointments = Appointment.objects.filter(slot__date=today).exclude(status='completed')
        return Response(AppointmentSerializer(appointments, many=True).data)

    def patch(self, request, pk):
        # تغییر وضعیت (مثلاً از رزرو به اتاق انتظار یا پایان ویزیت)
        appointment = get_object_or_404(Appointment, pk=pk)
        new_status = request.data.get('status')
        if new_status in dict(Appointment.STATUS_CHOICES):
            appointment.status = new_status
            appointment.save()
            return Response({"message": "وضعیت نوبت آپدیت شد"})
        return Response({"error": "وضعیت نامعتبر"}, status=status.HTTP_400_BAD_REQUEST)


class ExternalScraperAPIView(APIView):
    """نمایش نوبت‌هایی که از سایت‌های دیگر اسکرپ شده‌اند"""

    def get(self, request):
        external_data = Appointment.objects.filter(source='scraper').order_by('-slot__date')
        return Response(AppointmentSerializer(external_data, many=True).data)