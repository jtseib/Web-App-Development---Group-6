from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('client-profile/', views.client_profile, name='client_profile'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('sessions/', views.client_sessions, name='client_sessions'),
    path('cancel-session/', views.cancel_session, name='cancel_session'),
    path('reschedule-session/', views.reschedule_session, name='reschedule_session'),

    path('trainers/', views.trainers, name='trainers'),
    path('workouts/', views.workouts, name='workouts'),
    path('hours/', views.hours, name='hours'),
    path('hours/update/<int:pk>/', views.update_hours, name='update_hours'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('hours/create/<int:pk>/', views.create_hours, name='create_hours'),
]