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
    path('hours/update/<int:pk>/', views.UpdateHours.as_view(), name='update_hours'),
    path('calendar/', views.MonthlyCalendarView.as_view(), name='calendar_month'),
    path('hours/create/<int:year>/<int:month>/<int:day>/',views.CreateHours.as_view(),name='create_hours'),
]
