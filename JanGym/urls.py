from django.urls import path
from django.views.generic import detail

from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('client-profile/', views.client_profile, name='client_profile'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('sessions/', views.client_sessions, name='client_sessions'),
# CORRECT - use uuid
    path('cancel-session/', views.cancel_session, name='cancel_session'),
    path('reschedule-session/', views.reschedule_session, name='reschedule_session'),
    path('trainers/', views.trainers, name='trainers'),
    path('workouts/', views.workouts, name='workouts'),

    path('hours/', views.HoursListView.as_view(), name='hours'),
    path('calendar/', views.MonthlyCalendarView.as_view(), name='calendar_month'),
    path('hours/update/<int:pk>/', views.UpdateHours.as_view(), name='update_hours'),
    path('hours/create/<int:year>/<int:month>/<int:day>/', views.CreateHours.as_view(), name='create_hours'),
    path('progress/', views.log_workout_progress, name='log_workout_progress'),
    path('signup/', views.signup, name='signup'),
]