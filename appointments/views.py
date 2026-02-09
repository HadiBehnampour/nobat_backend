from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta
from .models import TimeSlot, Appointment
from .serializers import TimeSlotSerializer, AppointmentSerializer


class SlotManagerAPIView(APIView):
    """مدیریت اسلات‌های زمانی"""

    def get(self, request):
        """دریافت اسلات‌های یک روز"""
        date_param = request.query_params.get('date')

        if date_param:
            gregorian_date = TimeSlot.convert_jalali_to_gregorian(date_param)

            if not gregorian_date:
                return Response(
                    {
                        "error": "فرمت تاریخ نامعتبر است",
                        "expected_format": "1403/10/16",
                        "supported_formats": ["1403/10/16", "1403-10-16", "1403.10.16", "14031016"],
                        "received": date_param
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            slots = TimeSlot.objects.filter(date=gregorian_date).order_by('start_time')
        else:
            slots = TimeSlot.objects.all().order_by('date', 'start_time')

        serializer = TimeSlotSerializer(slots, many=True)
        return Response(serializer.data)

    def post(self, request):
        """ایجاد اسلات‌های زمانی برای یک روز"""
        date_param = request.data.get('date')
        start_time_str = request.data.get('start_time')
        end_time_str = request.data.get('end_time')
        interval = request.data.get('interval')

        if not all([date_param, start_time_str, end_time_str, interval]):
            return Response(
                {
                    "error": "تمام فیلدها الزامی هستند",
                    "required_fields": ["date", "start_time", "end_time", "interval"],
                    "example": {"date": "1403/10/16", "start_time": "10:00", "end_time": "17:00", "interval": 30}
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            interval = int(interval)
            if interval <= 0 or interval > 480:
                raise ValueError("بازه باید بین 1 و 480 دقیقه باشد")
        except (ValueError, TypeError) as e:
            return Response(
                {"error": f"مقدار interval نامعتبر است: {str(e)}", "received": str(interval), "valid_range": "1-480"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            gregorian_date = TimeSlot.convert_jalali_to_gregorian(date_param)

            if not gregorian_date:
                return Response(
                    {"error": "فرمت تاریخ نامعتبر است", "expected_format": "1403/10/16", "received": date_param},
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                start = datetime.strptime(start_time_str, '%H:%M')
                end = datetime.strptime(end_time_str, '%H:%M')
            except ValueError:
                return Response(
                    {"error": "فرمت ساعت نامعتبر است", "expected_format": "HH:MM", "example": "10:00"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if start >= end:
                return Response(
                    {"error": "ساعت شروع باید قبل از ساعت پایان باشد", "start_time": start_time_str,
                     "end_time": end_time_str},
                    status=status.HTTP_400_BAD_REQUEST
                )

            new_slots = []
            existing_slots = []
            current = start

            while current < end:
                slot, created = TimeSlot.objects.get_or_create(
                    date=gregorian_date,
                    start_time=current.time(),
                    defaults={'is_blocked': False}
                )

                if created:
                    new_slots.append(slot)
                else:
                    existing_slots.append(slot)

                current += timedelta(minutes=interval)

            serializer = TimeSlotSerializer(new_slots, many=True)

            return Response(
                {
                    "message": f"✅ عملیات موفقیت‌آمیز بود",
                    "summary": {
                        "total_slots_processed": len(new_slots) + len(existing_slots),
                        "new_slots_created": len(new_slots),
                        "existing_slots": len(existing_slots),
                        "date": {"jalali": date_param, "gregorian": str(gregorian_date)},
                        "start_time": start_time_str,
                        "end_time": end_time_str,
                        "interval_minutes": interval,
                        "calculation": f"از {start_time_str} تا {end_time_str} هر {interval} دقیقه = {len(new_slots) + len(existing_slots)} نوبت"
                    },
                    "new_slots": serializer.data,
                    "warning": f"⚠️ {len(existing_slots)} اسلات قبلاً وجود داشت" if existing_slots else None
                },
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {"error": f"خطای غیرمنتظره: {str(e)}", "error_type": type(e).__name__},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AppointmentBookingAPIView(APIView):
    """رزرو نوبت جدید"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        slot_id = request.data.get('slot_id')

        if not slot_id:
            return Response({"error": "slot_id الزامی است"}, status=status.HTTP_400_BAD_REQUEST)

        slot = get_object_or_404(TimeSlot, id=slot_id)

        if Appointment.objects.filter(slot=slot).exists() or slot.is_blocked:
            return Response(
                {"error": "این نوبت پر یا بسته است", "slot_id": slot_id, "is_available": False},
                status=status.HTTP_400_BAD_REQUEST
            )

        appointment = Appointment.objects.create(
            patient=request.user,
            slot=slot,
            source=request.data.get('source', 'site'),
            booking_type=request.data.get('booking_type', 'in_person'),
            price=request.data.get('price', 0),
            visit_reason=request.data.get('visit_reason', '')
        )

        serializer = AppointmentSerializer(appointment)
        return Response(
            {"message": "✅ نوبت شما با موفقیت ثبت شد", "appointment": serializer.data},
            status=status.HTTP_201_CREATED
        )


class WaitingRoomAPIView(APIView):
    """مدیریت اتاق انتظار"""

    def get(self, request):
        today = datetime.today().date()
        appointments = Appointment.objects.filter(
            slot__date=today
        ).exclude(
            status__in=['completed', 'canceled']
        ).order_by('slot__start_time')

        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)

    def patch(self, request, pk):
        appointment = get_object_or_404(Appointment, pk=pk)
        new_status = request.data.get('status')

        if new_status not in dict(Appointment.STATUS_CHOICES):
            return Response(
                {
                    "error": "وضعیت نامعتبر است",
                    "valid_statuses": [choice[0] for choice in Appointment.STATUS_CHOICES],
                    "received": new_status
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        appointment.status = new_status
        if request.data.get('notes'):
            appointment.notes = request.data.get('notes')
        appointment.save()

        serializer = AppointmentSerializer(appointment)
        return Response({"message": "✅ وضعیت نوبت بروزرسانی شد", "appointment": serializer.data})


class AdminAppointmentsListAPIView(APIView):
    """لیست نوبت‌ها برای ادمین"""

    def get(self, request):
        date = request.query_params.get('date')
        status_filter = request.query_params.get('status')

        appointments = Appointment.objects.all()

        if date:
            gregorian_date = TimeSlot.convert_jalali_to_gregorian(date)
            if gregorian_date:
                appointments = appointments.filter(slot__date=gregorian_date)
            else:
                return Response({"error": "فرمت تاریخ نامعتبر است"}, status=status.HTTP_400_BAD_REQUEST)

        if status_filter:
            if status_filter not in dict(Appointment.STATUS_CHOICES):
                return Response({"error": "وضعیت نامعتبر است"}, status=status.HTTP_400_BAD_REQUEST)
            appointments = appointments.filter(status=status_filter)

        appointments = appointments.order_by('-slot__date', 'slot__start_time')
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)


class AdminAppointmentDetailAPIView(APIView):
    """جزئیات نوبت برای ادمین"""

    def get(self, request, pk):
        appointment = get_object_or_404(Appointment, pk=pk)
        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data)

    def put(self, request, pk):
        appointment = get_object_or_404(Appointment, pk=pk)
        serializer = AppointmentSerializer(appointment, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminPatientAppointmentsAPIView(APIView):
    """نوبت‌های یک بیمار"""

    def get(self, request, patient_id):
        appointments = Appointment.objects.filter(patient_id=patient_id).order_by('-slot__date')
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)