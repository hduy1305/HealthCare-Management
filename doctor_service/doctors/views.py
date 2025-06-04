from django.shortcuts import render, redirect
from .models import Doctor,FullName
from .forms import DoctorForm, FullNameForm, AddressForm
from .models import Speciality
from .forms import SpecialityForm
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework import generics
from .models import Doctor, FullName, Address, Speciality
from .serializers import (
    DoctorSerializer,
    FullNameSerializer,
    AddressSerializer,
    SpecialitySerializer
)

def home(request):
    return render(request, 'doctors/home.html')

def doctor_list(request):
    doctors = Doctor.objects.select_related('fullname', 'address', 'speciality').all()
    return render(request, 'doctors/doctor_list.html', {'doctors': doctors})

def add_doctor(request):
    if request.method == 'POST':
        doctor_form = DoctorForm(request.POST)
        fullname_form = FullNameForm(request.POST)
        address_form = AddressForm(request.POST)

        if doctor_form.is_valid() and fullname_form.is_valid() and address_form.is_valid():
            fullname = fullname_form.save()
            address = address_form.save()
            doctor = doctor_form.save(commit=False)
            doctor.fullname = fullname
            doctor.address = address
            doctor.save()
            return redirect('doctor_list')
    else:
        doctor_form = DoctorForm()
        fullname_form = FullNameForm()
        address_form = AddressForm()

    return render(request, 'doctors/doctor_form.html', {
        'doctor_form': doctor_form,
        'fullname_form': fullname_form,
        'address_form': address_form,
    })

def speciality_list(request):
    specialities = Speciality.objects.all()
    return render(request, 'doctors/speciality_list.html', {'specialities': specialities})

def add_speciality(request):
    if request.method == 'POST':
        form = SpecialityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('speciality_list')
    else:
        form = SpecialityForm()
    return render(request, 'doctors/speciality_form.html', {'form': form, 'title': 'Thêm chuyên khoa'})

def edit_speciality(request, pk):
    speciality = get_object_or_404(Speciality, pk=pk)
    if request.method == 'POST':
        form = SpecialityForm(request.POST, instance=speciality)
        if form.is_valid():
            form.save()
            return redirect('speciality_list')
    else:
        form = SpecialityForm(instance=speciality)
    return render(request, 'doctors/speciality_form.html', {'form': form, 'title': 'Chỉnh sửa chuyên khoa'})

def delete_speciality(request, pk):
    speciality = get_object_or_404(Speciality, pk=pk)
    if request.method == 'POST':
        speciality.delete()
        return redirect('speciality_list')
    return render(request, 'doctors/speciality_confirm_delete.html', {'speciality': speciality})


def get_all_doctors(request):
    doctors = list(Doctor.objects.values())
    return JsonResponse(doctors, safe=False)


class DoctorListAPIView(generics.ListAPIView):
    """List all doctors"""
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

class DoctorDetailAPIView(generics.RetrieveAPIView):
    """Retrieve a specific doctor by ID"""
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    lookup_field = 'id'

class FullNameDetailAPIView(generics.RetrieveAPIView):
    """Retrieve full name detail by ID"""
    queryset = FullName.objects.all()
    serializer_class = FullNameSerializer
    lookup_field = 'id'

class AddressDetailAPIView(generics.RetrieveAPIView):
    """Retrieve address detail by ID"""
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    lookup_field = 'id'

class SpecialityListAPIView(generics.ListAPIView):
    """List all specialities"""
    queryset = Speciality.objects.all()
    serializer_class = SpecialitySerializer

class SpecialityDetailAPIView(generics.RetrieveAPIView):
    """Retrieve a specific speciality by ID"""
    queryset = Speciality.objects.all()
    serializer_class = SpecialitySerializer
    lookup_field = 'id'

def delete_doctor(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    if request.method == 'POST':
        doctor.delete()
    return redirect('doctor_list')