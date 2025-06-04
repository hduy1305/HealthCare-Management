from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from .models import Patient,Outpatient, Inpatient, MedicalHistory, FullName, Address, Emergency
from .forms import FullNameForm, AddressForm, OutpatientForm, InpatientForm, EmergencyForm
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse
from rest_framework import generics
from .models import Patient
from .models import FullName
from .serializers import FullNameSerializer
from .serializers import (
    BasePatientSerializer, FullNameSerializer,
    OutpatientSerializer, InpatientSerializer,
    EmergencySerializer, MedicalHistorySerializer
)



class GetPatientProfile(View):
    def get(self, request, patient_id):
        patient, patient_type = get_patient_and_type(patient_id)
        if not patient:
            return render(request, 'patients/patient_not_found.html', status=404)
        return render(request, 'patients/patient_profile.html', {
            'patient': patient,
            'patient_type': patient_type
        })


class UpdatePatientProfile(View):
    def get(self, request, patient_id):
        patient = Outpatient.objects.filter(pk=patient_id).first() or Inpatient.objects.filter(pk=patient_id).first() or  Emergency.objects.filter(pk=patient_id).first()
        if not patient:
            return render(request, 'patients/patient_not_found.html', status=404)
        fullname_form = FullNameForm(instance=patient.fullname)
        address_form = AddressForm(instance=patient.address)
        patient_form = OutpatientForm(instance=patient) if isinstance(patient, Outpatient) else InpatientForm(instance=patient) if isinstance(patient, Inpatient) else EmergencyForm(instance=patient)
        return render(request, 'patients/update_patient_profile.html', {
            'fullname_form': fullname_form,
            'address_form': address_form,
            'patient_form': patient_form,
            'patient': patient,
        })

    def post(self, request, patient_id):
        patient = Outpatient.objects.filter(pk=patient_id).first() or Inpatient.objects.filter(pk=patient_id).first() or Emergency.objects.filter(pk=patient_id).first()
        if not patient:
            return render(request, 'patients/patient_not_found.html', status=404)

        fullname_form = FullNameForm(request.POST, instance=patient.fullname)
        address_form = AddressForm(request.POST, instance=patient.address)
        patient_form_class = OutpatientForm if isinstance(patient, Outpatient) else InpatientForm if isinstance(patient, Inpatient) else EmergencyForm
        patient_form = patient_form_class(request.POST, instance=patient)

        if fullname_form.is_valid() and address_form.is_valid() and patient_form.is_valid():
            fullname_form.save()
            address_form.save()
            patient_form.save()
            return redirect('get_patient_profile', patient_id=patient.id)

        return render(request, 'patients/update_patient_profile.html', {
            'fullname_form': fullname_form,
            'address_form': address_form,
            'patient_form': patient_form,
            'patient': patient,
        })

class ListPatientHistory(View):
    def get(self, request, patient_id):
        # Có thể tìm trong Outpatient hoặc Inpatient
        patient = Outpatient.objects.filter(pk=patient_id).first() or Inpatient.objects.filter(pk=patient_id).first() or Emergency.objects.filter(pk=patient_id).first()
        if not patient:
            return render(request, 'patients/patient_not_found.html', status=404)
        history_list = MedicalHistory.objects.filter(patient_id=patient.id).order_by('-visit_date')
        return render(request, 'patients/patient_history.html', {
            'patient': patient,
            'history_list': history_list,
        })

class GetPatientByID(View):
    def get(self, request, patient_id):
        # Tương tự GetPatientProfile
        patient = Outpatient.objects.filter(pk=patient_id).first() or Inpatient.objects.filter(pk=patient_id).first() or Emergency.objects.filter(pk=patient_id).first()
        if not patient:
            return render(request, 'patients/patient_not_found.html', status=404)
        return render(request, 'patients/patient_profile.html', {'patient': patient})

def dashboard(request):
    patient_type = request.GET.get('patient_type', '')  # lấy giá trị lọc từ query param

    if patient_type == 'outpatient':
        patients = Patient.objects.filter(outpatient__isnull=False)
    elif patient_type == 'inpatient':
        patients = Patient.objects.filter(inpatient__isnull=False)
    elif patient_type == 'emergency':
        patients = Patient.objects.filter(emergency__isnull=False)
    else:
        patients = Patient.objects.all()

    return render(request, 'patients/patient_dashboard.html', {'patients': patients, 'selected_type': patient_type})

def get_patient_and_type(patient_id):
    for model, type_str in [(Outpatient, 'outpatient'), (Inpatient, 'inpatient'), (Emergency, 'emergency')]:
        patient = model.objects.filter(pk=patient_id).first()
        if patient:
            return patient, type_str
    return None, None

@require_POST
def delete_patient(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)
    patient.delete()
    messages.success(request, "Đã xóa bệnh nhân thành công.")
    return redirect('dashboard')

def add_patient(request):
    patient_type = request.GET.get('type')

    PATIENT_TYPE_VN = {
        'outpatient': 'Ngoại trú',
        'inpatient': 'Nội trú',
        'emergency': 'Cấp cứu',
    }
    patient_type_vn = PATIENT_TYPE_VN.get(patient_type, 'Không xác định')

    if request.method == 'POST':
        fullname_form = FullNameForm(request.POST)
        address_form = AddressForm(request.POST)

        if patient_type == 'outpatient':
            patient_form = OutpatientForm(request.POST)
        elif patient_type == 'inpatient':
            patient_form = InpatientForm(request.POST)
        elif patient_type == 'emergency':
            patient_form = EmergencyForm(request.POST)
        else:
            patient_form = None

        if fullname_form.is_valid() and address_form.is_valid() and patient_form and patient_form.is_valid():
            # Lưu fullname và address trước (giả sử tách ra model riêng)
            fullname = fullname_form.save()
            address = address_form.save()

            # Lưu bệnh nhân (chưa commit để gán fullname và address)
            patient = patient_form.save(commit=False)
            patient.fullname = fullname
            patient.address = address
            patient.patient_type = patient_type_vn
            patient.save()

            # Sau khi lưu thành công, redirect về trang chi tiết hoặc danh sách
            return redirect('get_patient_profile', patient_id=patient.id)
        else:
            # Nếu có lỗi validate thì sẽ hiển thị lại form với lỗi
            context = {
                'patient_type': patient_type_vn,
                'patient_form': patient_form,
                'fullname_form': fullname_form,
                'address_form': address_form,
            }
            return render(request, 'patients/add_patient.html', context)

    else:
        # GET request, tạo form rỗng
        fullname_form = FullNameForm()
        address_form = AddressForm()

        if patient_type == 'outpatient':
            patient_form = OutpatientForm()
        elif patient_type == 'inpatient':
            patient_form = InpatientForm()
        elif patient_type == 'emergency':
            patient_form = EmergencyForm()
        else:
            patient_form = None

    context = {
        'patient_type': patient_type_vn,
        'patient_form': patient_form,
        'fullname_form': fullname_form,
        'address_form': address_form,
    }
    return render(request, 'patients/add_patient.html', context)

# def get_all_patients(request):
#     patients = list(Patient.objects.values())
#     return JsonResponse(patients, safe=False)

class PatientListAPIView(generics.ListAPIView):
    """API view to list all patients"""
    queryset = Patient.objects.all()
    serializer_class = BasePatientSerializer

class PatientDetailAPIView(generics.RetrieveAPIView):
    """API view to retrieve a single patient by ID"""
    queryset = Patient.objects.all()
    serializer_class = BasePatientSerializer
    lookup_field = 'id'

class FullNameDetailAPIView(generics.RetrieveAPIView):
    """API view to retrieve a full name detail by ID"""
    queryset = FullName.objects.all()
    serializer_class = FullNameSerializer
    lookup_field = 'id'

class OutpatientListAPIView(generics.ListAPIView):
    """List all outpatients"""
    queryset = Outpatient.objects.all()
    serializer_class = OutpatientSerializer

class InpatientListAPIView(generics.ListAPIView):
    """List all inpatients"""
    queryset = Inpatient.objects.all()
    serializer_class = InpatientSerializer

class EmergencyListAPIView(generics.ListAPIView):
    """List all emergency patients"""
    queryset = Emergency.objects.all()
    serializer_class = EmergencySerializer

class MedicalHistoryListAPIView(generics.ListAPIView):
    """List all medical history records"""
    queryset = MedicalHistory.objects.all()
    serializer_class = MedicalHistorySerializer

class PatientMedicalHistoryListAPIView(generics.ListAPIView):
    """List medical history for a specific patient"""
    serializer_class = MedicalHistorySerializer

    def get_queryset(self):
        patient_id = self.kwargs['patient_id']
        return MedicalHistory.objects.filter(patient_id=patient_id)