from django.urls import path
from .views import SlotManagerAPIView, AppointmentBookingAPIView, WaitingRoomAPIView, ExternalScraperAPIView

urlpatterns = [
    path('slots/', SlotManagerAPIView.as_view(), name='slot_manager'),
    path('book/', AppointmentBookingAPIView.as_view(), name='book_appointment'),
    path('waiting-room/', WaitingRoomAPIView.as_view(), name='waiting_room'),
    path('waiting-room/<int:pk>/', WaitingRoomAPIView.as_view(), name='update_status'),
    path('scraper/', ExternalScraperAPIView.as_view(), name='scraper_view'),
]