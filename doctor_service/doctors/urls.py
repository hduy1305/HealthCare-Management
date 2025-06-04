from django.urls import path
from . import views
from django.shortcuts import redirect
from .views import DoctorListAPIView, FullNameDetailAPIView, DoctorDetailAPIView

urlpatterns = [
    path('', views.home, name='doctor_home'),
    path('doctors/', views.doctor_list, name='doctor_list'),
    path('doctors/add/', views.add_doctor, name='add_doctor'),
    path('api/doctors/', DoctorListAPIView.as_view(), name='doctor-list'),
    path('api/doctors/<int:id>/', DoctorDetailAPIView.as_view(), name='doctor-detail'),
    path('api/fullnames/<int:id>/', FullNameDetailAPIView.as_view(), name='fullname-detail'),
    path('doctors/delete/<int:doctor_id>/', views.delete_doctor, name='delete_doctor'),


        # Speciality CRUD
    path('specialities/', views.speciality_list, name='speciality_list'),
    path('specialities/add/', views.add_speciality, name='add_speciality'),
    path('specialities/<int:pk>/edit/', views.edit_speciality, name='edit_speciality'),
    path('specialities/<int:pk>/delete/', views.delete_speciality, name='delete_speciality'),
]
