from rest_framework import serializers
from .models import OfficeSettings, WorkingHour

class OfficeSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfficeSettings
        fields = '__all__'

class WorkingHourSerializer(serializers.ModelSerializer):
    day_display = serializers.CharField(source='get_day_display', read_only=True)

    class Meta:
        model = WorkingHour
        fields = ['id', 'day', 'day_display', 'start_time', 'end_time', 'is_active']