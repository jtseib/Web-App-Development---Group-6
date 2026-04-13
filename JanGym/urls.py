from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('trainers/', views.trainers, name='trainers'),
    path('workouts/', views.workouts, name='workouts'),
    path('client-profile/', views.client_profile, name='client_profile'),
    path('hours/', views.HoursListView.as_view(), name='gym_hours'),
    path('hours/update/<int:pk>/', views.UpdateHours.as_view(), name='update_hours'),
    path('calendar/', views.MonthlyCalendarView.as_view(), name='calendar_month'),
    path('calendar/<int:year>/<int:month>/', views.MonthlyCalendarView.as_view(), name='calendar_month'),
    path('hours/create/<int:year>/<int:month>/<int:day>/', views.CreateHours.as_view(), name='create_hours'),

]
