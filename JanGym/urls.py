from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("client-profile/", views.client_profile, name="client_profile"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path('sessions/', views.client_sessions, name='client_sessions'),
    path('cancel-session/', views.cancel_session, name='cancel_session'),
    path('reschedule-session/', views.reschedule_session, name='reschedule_session'),

]
