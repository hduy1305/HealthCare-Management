from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from django.utils.dateparse import parse_datetime
from django.urls import reverse
from .models import Appointment
from .utils import get_patients, get_doctors
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.shortcuts import redirect
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Type, Room, Appointment
from .serializers import TypeSerializer, RoomSerializer, AppointmentSerializer

import requests
import json

# Giữ nguyên các API hiện tại

DOCTOR_SERVICE_URL = "http://doctor-service:8000/api/doctors/"
PATIENT_SERVICE_URL = "http://patient-service:8000/api/patients/"

def home(request):
    return render(request, 'appointments/home.html')

def list_appointments_by_user(request, user_type, user_id):
    if user_type not in ('patient', 'doctor'):
        return HttpResponseBadRequest("Invalid user_type")

    if user_type == 'patient':
        appts = Appointment.objects.filter(patient_id=user_id)
    else:
        appts = Appointment.objects.filter(doctor_id=user_id)

    data = []
    for a in appts:
        data.append({
            'id': a.id,
            'patient_name': a.patient_name,
            'doctor_name': a.doctor_name,
            'appointment_time': a.appointment_time.isoformat(),
            'status': a.status,
        })
    return JsonResponse(data, safe=False)


@csrf_exempt
def cancel_appointment(request, appt_id):
    if request.method != 'POST':
        return HttpResponseBadRequest("Only POST method allowed")

    try:
        appt = Appointment.objects.get(id=appt_id)
    except Appointment.DoesNotExist:
        return HttpResponseNotFound("Appointment not found")

    appt.status = 'cancelled'
    appt.save()
    return JsonResponse({'id': appt.id, 'status': appt.status})


@csrf_exempt
def update_appointment_status(request, appt_id):
    if request.method != 'POST':
        return HttpResponseBadRequest("Only POST method allowed")

    data = json.loads(request.body)
    new_status = data.get('status')
    valid_statuses = ['pending', 'confirmed', 'completed', 'cancelled', 'rejected']
    if new_status not in valid_statuses:
        return HttpResponseBadRequest("Invalid status")

    try:
        appt = Appointment.objects.get(id=appt_id)
    except Appointment.DoesNotExist:
        return HttpResponseNotFound("Appointment not found")

    appt.status = new_status
    appt.save()
    return JsonResponse({'id': appt.id, 'status': appt.status})


# === VIEWS RENDER TEMPLATES ===

def create_appointment(request):
    print("Request method:", request.method)
    if request.method == 'GET':
        print("Render create form GET")
        return render(request, 'appointments/create_appointment.html')

    if request.method == 'POST':
        print("Process POST data")
        patient_id = request.POST.get('patient_id')
        doctor_id = request.POST.get('doctor_id')
        appt_time_str = request.POST.get('appointment_time')
        print(f"patient_id={patient_id}, doctor_id={doctor_id}, appointment_time={appt_time_str}")

        if not all([patient_id, doctor_id, appt_time_str]):
            print("Missing some POST fields")
            return render(request, 'appointments/create_appointment.html', {
                'error': 'Vui lòng điền đầy đủ thông tin.'
            })

        appointment_time = parse_datetime(appt_time_str)
        print("Parsed appointment_time:", appointment_time)
        if not appointment_time:
            print("Invalid appointment_time")
            return render(request, 'appointments/create_appointment.html', {
                'error': 'Thời gian không hợp lệ.'
            })

        try:
            
            resp = requests.get(f"{PATIENT_SERVICE_URL}{patient_id}/", timeout=5)
            print("Fetching patient from:", f"{PATIENT_SERVICE_URL}{patient_id}/")
            resp.raise_for_status()
            patient = resp.json()
            print("Got patient:", patient)
        except requests.RequestException:
            print("Failed to fetch patient info")
            return render(request, 'appointments/create_appointment.html', {
                'error': 'Không lấy được thông tin bệnh nhân.'
            })

        try:
            resp = requests.get(f"{DOCTOR_SERVICE_URL}{doctor_id}/", timeout=5)
            resp.raise_for_status()
            doctor = resp.json()
            print("Got doctor:", doctor)
        except requests.RequestException:
            print("Failed to fetch doctor info")
            return render(request, 'appointments/create_appointment.html', {
                'error': 'Không lấy được thông tin bác sĩ.'
            })

        appt = Appointment.objects.create(
            patient_id=patient_id,
            doctor_id=doctor_id,
            appointment_time=appointment_time,
            patient_name=patient.get('full_name_str', 'Unknown'),
            doctor_name=doctor.get('full_name_str', 'Unknown'),
        )
        print(f"Appointment created, id={appt.id}")

        print(f"Redirecting to appointment_detail with id={appt.id}")
        return redirect('appointment_detail', appt.id)


def list_appointments_view(request, user_type, user_id):
    # 1. Kiểm tra user_type hợp lệ
    if user_type not in ('patient', 'doctor'):
        return HttpResponseBadRequest("Invalid user_type")

    # 2. Gọi API để kiểm tra xem patient/doctor có tồn tại không
    try:
        if user_type == 'patient':
            resp = requests.get(f"{PATIENT_SERVICE_URL}{user_id}/", timeout=5)
        else:
            resp = requests.get(f"{DOCTOR_SERVICE_URL}{user_id}/", timeout=5)

        # Nếu trả về 404 → xử lý như kiểu “not found”
        if resp.status_code == 404:
            return render(request, 'appointments/user_not_found.html', {
                'user_type': user_type,
                'user_id': user_id
            })
        # Nếu có lỗi khác (5xx, 4xx, timeout, ...) cũng tính là “not found” hoặc lỗi service
        resp.raise_for_status()

    except requests.RequestException:
        # Khi không kết nối được hoặc API trả về lỗi, hiển thị tương tự “not found”
        return render(request, 'appointments/user_not_found.html', {
            'user_type': user_type,
            'user_id': user_id
        })

    # 3. Nếu tồn tại, lấy danh sách appointments từ database
    if user_type == 'patient':
        appts = Appointment.objects.filter(patient_id=user_id).order_by('-appointment_time')
    else:
        appts = Appointment.objects.filter(doctor_id=user_id).order_by('-appointment_time')

    return render(request, 'appointments/list_appointments.html', {
        'appointments': appts,
        'user_type': user_type,
        'user_id': user_id,
    })


def appointment_detail_view(request, appt_id):
    appt = get_object_or_404(Appointment, id=appt_id)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'cancel':
            appt.status = 'cancelled'
            appt.save()
        elif action in ['pending', 'confirmed', 'completed', 'rejected']:
            appt.status = action
            appt.save()
        
        return HttpResponseRedirect(reverse('appointment_detail', args=[appt.id]))

    return render(request, 'appointments/appointment_detail.html', {
        'appointment': appt,
    })


def update_status_view(request, appt_id):
    appt = get_object_or_404(Appointment, id=appt_id)
    error = None
    valid_statuses = ['pending', 'confirmed', 'completed', 'cancelled', 'rejected']

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status not in valid_statuses:
            error = "Invalid status"
        else:
            appt.status = new_status
            appt.save()
            # Chú ý: namespace 'appointments' nếu bạn include URLs với namespace
            return HttpResponseRedirect(reverse('appointment_detail', args=[appt.id]))

    return render(request, 'appointments/update_status.html', {
        'appointment': appt,
        'error': error,
        'valid_statuses': valid_statuses,
    })


def cancel_appointment_view(request, appt_id):
    appt = get_object_or_404(Appointment, id=appt_id)
    if request.method == 'POST':
        appt.status = 'cancelled'
        appt.save()
        return HttpResponseRedirect(reverse('appointment_detail', args=[appt.id]))
    return render(request, 'appointments/cancel_appointment.html', {
        'appointment': appt
    })


# --- ViewSets cho Type, Room, Appointment ---
class TypeViewSet(viewsets.ModelViewSet):
    """
    /api/types/         -> GET list, POST create
    /api/types/{pk}/    -> GET retrieve, PUT/PATCH update, DELETE destroy
    """
    queryset = Type.objects.all()
    serializer_class = TypeSerializer


class RoomViewSet(viewsets.ModelViewSet):
    """
    /api/rooms/         -> GET list, POST create
    /api/rooms/{pk}/    -> GET retrieve, PUT/PATCH update, DELETE destroy
    """
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class AppointmentViewSet(viewsets.ModelViewSet):
    """
    /api/appointments/         -> GET list, POST create
    /api/appointments/{pk}/    -> GET retrieve, PUT/PATCH update, DELETE destroy
    """
    queryset = Appointment.objects.all().order_by('-appointment_time')
    serializer_class = AppointmentSerializer


# --- Nếu bạn muốn giữ function-based views, có thể thêm thêm: ---

@api_view(['GET', 'POST'])
def appointment_list_api(request):
    """
    GET  /api/appointments/         -> list all appointments
    POST /api/appointments/         -> create new appointment
    """
    if request.method == 'GET':
        appts = Appointment.objects.all().order_by('-appointment_time')
        serializer = AppointmentSerializer(appts, many=True)
        return Response(serializer.data)

    # POST
    serializer = AppointmentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def appointment_detail_api(request, pk):
    """
    GET    /api/appointments/{pk}/    -> retrieve one
    PUT    /api/appointments/{pk}/    -> update all fields
    DELETE /api/appointments/{pk}/    -> delete
    """
    try:
        appt = Appointment.objects.get(pk=pk)
    except Appointment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AppointmentSerializer(appt)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = AppointmentSerializer(appt, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        appt.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
