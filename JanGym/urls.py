from django.urls import path
from . import views

urlpatterns = [

    # ---------------------------------------------------------
    # PUBLIC / GENERAL
    # ---------------------------------------------------------
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),

    # ---------------------------------------------------------
    # MEMBER DASHBOARD + MEMBER FEATURES
    # ---------------------------------------------------------
    path('dashboard/', views.dashboard, name='dashboard'),  # MEMBER dashboard
    path('client-profile/', views.client_profile, name='client_profile'),
    path('sessions/', views.client_sessions, name='client_sessions'),
    path('cancel-session/', views.cancel_session, name='cancel_session'),
    path('reschedule-session/', views.reschedule_session, name='reschedule_session'),

    # Member booking system
    path("client/available/", views.client_available_sessions, name="client_available_sessions"),
    path("client/available/<int:year>/<int:week>/", views.client_available_sessions, name="client_available_sessions_week"),
    path("client/book/<int:slot_id>/", views.book_session, name="book_session"),

    # ---------------------------------------------------------
    # TRAINER DASHBOARD + TRAINER FEATURES
    # ---------------------------------------------------------
    path("trainer/dashboard/", views.trainer_dashboard, name="trainer_dashboard"),
    path("trainer/calendar/", views.trainer_calendar, name="trainer_calendar"),
    path("trainer/calendar/<int:year>/<int:week>/", views.trainer_calendar, name="trainer_calendar_week"),

    # Trainer availability
    path('trainer/availability/', views.trainer_availability, name='trainer_availability'),
    path('trainer/availability/add/', views.add_availability, name='add_availability'),
    path('trainer/availability/default/', views.set_default_availability, name='set_default_availability'),

    # Trainer booking view (seeing what clients booked)
    path('sessions/available/', views.available_sessions, name='available_sessions'),

    # ---------------------------------------------------------
    # WORKOUTS / PROGRESS
    # ---------------------------------------------------------
    path('workouts/', views.workouts, name='workouts'),
    path('progress/', views.log_workout_progress, name='log_workout_progress'),

    # ---------------------------------------------------------
    # GYM HOURS (ADMIN)
    # ---------------------------------------------------------
    path('hours/', views.HoursListView.as_view(), name='hours'),
    path('calendar/', views.MonthlyCalendarView.as_view(), name='calendar_month'),
    path('hours/update/<int:pk>/', views.UpdateHours.as_view(), name='update_hours'),
    path('hours/create/<int:year>/<int:month>/<int:day>/', views.CreateHours.as_view(), name='create_hours'),
]
