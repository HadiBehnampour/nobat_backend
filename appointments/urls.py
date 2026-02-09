from django.urls import path
from .views import (
    SlotManagerAPIView,
    AppointmentBookingAPIView,
    WaitingRoomAPIView,
    AdminAppointmentsListAPIView,
    AdminAppointmentDetailAPIView,
    AdminPatientAppointmentsAPIView,
)

app_name = 'appointments'

urlpatterns = [
    # Slot Management
    path('slots/', SlotManagerAPIView.as_view(), name='slot_manager'),

    # Appointment Booking
    path('book/', AppointmentBookingAPIView.as_view(), name='book_appointment'),

    # Waiting Room
    path('waiting-room/', WaitingRoomAPIView.as_view(), name='waiting_room'),
    path('waiting-room/<int:pk>/', WaitingRoomAPIView.as_view(), name='update_status'),

    # Admin APIs
    path('admin/list/', AdminAppointmentsListAPIView.as_view(), name='admin_appointments_list'),
    path('admin/<int:pk>/', AdminAppointmentDetailAPIView.as_view(), name='admin_appointment_detail'),
    path('admin/patient/<int:patient_id>/', AdminPatientAppointmentsAPIView.as_view(),
         name='admin_patient_appointments'),
]