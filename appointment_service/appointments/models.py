from django.db import models
from django.contrib.auth.models import User

class Type(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Room(models.Model):
    number = models.CharField(max_length=20)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.number

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('rejected', 'Rejected'),
    ]

    patient_id = models.IntegerField()   # Lưu id patient từ patient-service
    patient_name = models.CharField(max_length=255)  # Tên lưu lại để dễ đọc
    doctor_id = models.IntegerField()    # Lưu id doctor từ doctor-service
    doctor_name = models.CharField(max_length=255)  # Tên doctor
    appointment_time = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Appointment {self.id} - Patient {self.patient_name} with Doctor {self.doctor_name} at {self.appointment_time}"
