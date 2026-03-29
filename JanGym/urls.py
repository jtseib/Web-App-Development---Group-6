from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('trainers/', views.trainers, name='trainers'),
    path('workouts/', views.workouts, name='workouts'),
    path('client-profile/', views.client_profile, name='client_profile'),
]
