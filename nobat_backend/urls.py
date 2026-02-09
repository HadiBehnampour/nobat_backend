"""
URL configuration for nobat_backend project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # API URLs
    path('api/appointments/', include('appointments.urls')),
    path('api/users/', include('users.urls')),
    path('api/consultations/', include('consultations.urls')),
    path('api/medical/', include('medical_records.urls')),
    path('api/finance/', include('finance.urls')),
    path('api/settings/', include('settings_config.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)