from rest_framework import serializers
from .models import Type, Room, Appointment

class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = ['id', 'name']


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'number', 'description']


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = [
            'id',
            'patient_id',
            'patient_name',
            'doctor_id',
            'doctor_name',
            'appointment_time',
            'status',
            'created_at',
        ]
        
        read_only_fields = ['created_at']
