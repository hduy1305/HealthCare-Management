# urls.py
from django.urls import path
from . import views
from django.shortcuts import redirect
from .views import  PatientDetailAPIView, PatientListAPIView, GetPatientProfile, UpdatePatientProfile, ListPatientHistory, GetPatientByID, FullNameDetailAPIView


urlpatterns = [
    path('', lambda request: redirect('patients/', permanent=False)),
    path('api/patients/', PatientListAPIView.as_view(), name='patient-list'),
    path('api/patients/<int:id>/', PatientDetailAPIView.as_view(), name='patient-detail'),
    path('api/fullnames/<int:id>/', FullNameDetailAPIView.as_view(), name='fullname-detail'),

    path('patients/', views.dashboard, name='dashboard'),
    path('patients/<int:patient_id>/', GetPatientProfile.as_view(), name='get_patient_profile'),
    path('patients/<int:patient_id>/update/', UpdatePatientProfile.as_view(), name='update_patient_profile'),
    path('patients/<int:patient_id>/history/', ListPatientHistory.as_view(), name='list_patient_history'),
    path('patients/by-id/<int:patient_id>/', GetPatientByID.as_view(), name='get_patient_by_id'),
    path('patients/delete/<int:patient_id>/', views.delete_patient, name='delete_patient'),
    path('patients/add/', views.add_patient, name='add_patient'),
]
