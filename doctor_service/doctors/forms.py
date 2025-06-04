from django import forms
from .models import Doctor, FullName, Address, Speciality

class FullNameForm(forms.ModelForm):
    class Meta:
        model = FullName
        fields = ['first_name', 'middle_name', 'last_name']

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['street', 'ward', 'district', 'city']

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['speciality', 'phone_number', 'email']

class SpecialityForm(forms.ModelForm):
    class Meta:
        model = Speciality
        fields = ['code', 'name', 'description']
