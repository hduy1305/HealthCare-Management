from django import forms
from .models import Outpatient, Inpatient, FullName, Address, Emergency

class FullNameForm(forms.ModelForm):
    class Meta:
        model = FullName
        fields = ['first_name', 'middle_name', 'last_name']

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['street', 'district', 'city', 'province']

class OutpatientForm(forms.ModelForm):
    class Meta:
        model = Outpatient
        fields = ['phone', 'email', 'date_of_birth', 'gender', 'visit_reason']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'class': 'datepicker', 'autocomplete': 'off'})
        }

class InpatientForm(forms.ModelForm):
    class Meta:
        model = Inpatient
        fields = ['phone', 'email', 'date_of_birth', 'gender', 'room_number', 'admission_date', 'discharge_date']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'class': 'datepicker', 'autocomplete': 'off'}),
            'admission_date': forms.DateInput(attrs={'class': 'datepicker', 'autocomplete': 'off'}),
            'discharge_date': forms.DateInput(attrs={'class': 'datepicker', 'autocomplete': 'off'}),
        }

class EmergencyForm(forms.ModelForm):
    class Meta:
        model = Emergency
        fields = ['phone', 'email', 'date_of_birth', 'gender', 'emergency_level', 'arrival_time', 'notes']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'class': 'datepicker', 'autocomplete': 'off'}),
            'arrival_time': forms.DateTimeInput(attrs={'class': 'datetimepicker', 'autocomplete': 'off'}),
        }
