from django.urls import path
from .views import appointment_list_api, appointment_detail_api
from . import views


urlpatterns = [
    path('', views.home, name='appointment_home'),
    path('appointments/create/', views.create_appointment, name='create_appointment'),
    path('appointments/detail/<int:appt_id>/', views.appointment_detail_view, name='appointment_detail'),
    path('appointments/update-status/<int:appt_id>/', views.update_status_view, name='update_status'),
    path('appointments/cancel/<int:appt_id>/', views.cancel_appointment_view, name='cancel_appointment'),
    path('appointments/<str:user_type>/<int:user_id>/', views.list_appointments_view, name='list_appointments'),

    path('api/appointments/', appointment_list_api, name='appointment_list_api'),
    path('api/appointments/<int:pk>/', appointment_detail_api, name='appointment_detail_api'),
]