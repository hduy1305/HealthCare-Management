# records/views.py
import requests
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from .models import MedicalRecord
from .forms import MedicalRecordForm

def _fetch_choices(url):
    """Helper: gọi HTTP GET và trả về list of dict."""
    try:
        r = requests.get(url)
        r.raise_for_status()
        return r.json()
    except requests.RequestException:
        return []

def record_list(request):
    qs = MedicalRecord.objects.filter(is_deleted=False).order_by('-created_at')
    return render(request, 'records/record_list.html', {'records': qs})

def record_detail(request, pk):
    record = get_object_or_404(MedicalRecord, pk=pk, is_deleted=False)
    return render(request, 'records/record_detail.html', {'record': record})

def record_create(request):
    # Lấy danh sách patients, doctors, appointments để chọn
    patients     = _fetch_choices(settings.PATIENT_SERVICE_URL)
    doctors      = _fetch_choices(settings.DOCTOR_SERVICE_URL)
    appointments = _fetch_choices(settings.APPOINTMENT_SERVICE_URL)

    if request.method == 'POST':
        form = MedicalRecordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('records:record_list')
    else:
        form = MedicalRecordForm()

    return render(request, 'records/record_form.html', {
        'form': form,
        'patients': patients,
        'doctors': doctors,
        'appointments': appointments,
    })

def record_update(request, pk):
    record = get_object_or_404(MedicalRecord, pk=pk, is_deleted=False)

    patients     = _fetch_choices(settings.PATIENT_SERVICE_URL)
    doctors      = _fetch_choices(settings.DOCTOR_SERVICE_URL)
    appointments = _fetch_choices(settings.APPOINTMENT_SERVICE_URL)

    if request.method == 'POST':
        form = MedicalRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect('records:record_detail', pk=pk)
    else:
        form = MedicalRecordForm(instance=record)

    return render(request, 'records/record_form.html', {
        'form': form,
        'patients': patients,
        'doctors': doctors,
        'appointments': appointments,
        'update': True,
    })

def record_delete(request, pk):
    record = get_object_or_404(MedicalRecord, pk=pk, is_deleted=False)
    if request.method == 'POST':
        record.is_deleted = True
        record.save()
        return redirect('records:record_list')
    return render(request, 'records/record_confirm_delete.html', {'record': record})
