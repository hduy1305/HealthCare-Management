from django.db import models

# Create your models here.


class Diagnosis(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Prescription(models.Model):
    medication_name = models.CharField(max_length=200)
    dosage = models.CharField(max_length=100)
    instruction = models.TextField(blank=True)

    def __str__(self):
        return f"{self.medication_name} ({self.dosage})"

class MedicalRecord(models.Model):
    patient_id     = models.IntegerField()
    doctor_id      = models.IntegerField()
    appointment_id = models.IntegerField()
    notes          = models.TextField(blank=True)
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)
    is_deleted     = models.BooleanField(default=False)

    diagnoses      = models.ManyToManyField(Diagnosis, blank=True)
    prescriptions  = models.ManyToManyField(Prescription, blank=True)

    def __str__(self):
        return f"MR#{self.id} - Patient {self.patient_id}"