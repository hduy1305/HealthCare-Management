# models.py
from django.db import models

class FullName(models.Model):
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.last_name} {self.middle_name} {self.first_name}".strip()

class Address(models.Model):
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    province = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.street}, {self.district}, {self.city}, {self.province}"

class Patient(models.Model):
    fullname = models.OneToOneField(FullName, on_delete=models.CASCADE)
    address = models.OneToOneField(Address, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_patient_type(self):
        if hasattr(self, 'outpatient'):
            return 'Ngoại trú'
        elif hasattr(self, 'inpatient'):
            return 'Nội trú'
        elif hasattr(self, 'emergency'):
            return 'Cấp cứu'
        else:
            return 'Không xác định'

class Outpatient(Patient):
    visit_reason = models.CharField(max_length=255)

class Inpatient(Patient):
    room_number = models.CharField(max_length=20)
    admission_date = models.DateField()
    discharge_date = models.DateField(null=True, blank=True)

class Emergency(Patient):
    emergency_level = models.CharField(max_length=50)  # Ví dụ mức độ khẩn cấp
    arrival_time = models.DateTimeField()              # Thời gian nhập viện khẩn cấp
    notes = models.TextField(blank=True, null=True)

class MedicalHistory(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    visit_date = models.DateField()
    diagnosis = models.TextField()
    treatment = models.TextField()
