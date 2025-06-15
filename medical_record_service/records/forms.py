# records/forms.py
from django import forms
from .models import MedicalRecord, Diagnosis, Prescription

class DiagnosisForm(forms.ModelForm):
    class Meta:
        model = Diagnosis
        fields = ['name', 'description']

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['medication_name', 'dosage', 'instruction']

class MedicalRecordForm(forms.ModelForm):
    diagnoses     = forms.ModelMultipleChoiceField(
        queryset=Diagnosis.objects.all(), required=False, widget=forms.CheckboxSelectMultiple
    )
    prescriptions = forms.ModelMultipleChoiceField(
        queryset=Prescription.objects.all(), required=False, widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = MedicalRecord
        fields = ['patient_id', 'doctor_id', 'appointment_id', 'notes', 'diagnoses', 'prescriptions']
