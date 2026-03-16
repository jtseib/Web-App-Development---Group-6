from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("client-profile/", views.client_profile, name="client_profile"),
    path("dashboard/", views.dashboard, name="dashboard"),
]
