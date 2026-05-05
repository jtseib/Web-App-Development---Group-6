from django.urls import path
from . import views

urlpatterns = [

    # Public
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),

    # Member dashboard + profile
    path('dashboard/', views.dashboard, name='dashboard'),
    path('client-profile/', views.client_profile, name='client_profile'),

    # Member sessions
    path('sessions/', views.client_sessions, name='client_sessions'),
    path('cancel-session/', views.cancel_session, name='cancel_session'),
    path('reschedule-session/', views.reschedule_session, name='reschedule_session'),

    # Trainer selection
    path("client/select-trainer/", views.select_trainer, name="select_trainer"),

    # Member: view trainer availability + book
    path("trainer/available/", views.trainer_available_sessions, name="trainer_available_sessions"),
    path("trainer/book/<int:slot_id>/", views.book_trainer_slot, name="book_trainer_slot"),

    # Trainer dashboard + calendar
    path("trainer/dashboard/", views.trainer_dashboard, name="trainer_dashboard"),
    path("trainer/calendar/", views.trainer_calendar, name="trainer_calendar"),
    path("trainer/calendar/<int:year>/<int:week>/", views.trainer_calendar, name="trainer_calendar_week"),

    # Trainer availability management
    path('trainer/availability/', views.trainer_availability, name='trainer_availability'),
    path('trainer/availability/add/', views.add_availability, name='add_availability'),
    path('trainer/availability/default/', views.set_default_availability, name='set_default_availability'),

    # Workouts
    path('workouts/', views.workouts, name='workouts'),
    path('progress/', views.log_workout_progress, name='log_workout_progress'),

    # Gym hours
    path('hours/', views.HoursListView.as_view(), name='hours'),
    path('calendar/', views.MonthlyCalendarView.as_view(), name='calendar_month'),
    path('hours/update/<int:pk>/', views.UpdateHours.as_view(), name='update_hours'),
    path('hours/create/<int:year>/<int:month>/<int:day>/', views.CreateHours.as_view(), name='create_hours'),

    # Member weekly availability calendar
    path("trainer/available/<int:year>/<int:week>/",views.trainer_available_calendar,name="trainer_available_calendar"),
    path("book/<int:slot_id>/", views.book_trainer_slot, name="book_trainer_slot"),
    path("trainer/client/<int:user_id>/", views.trainer_view_client, name="trainer_view_client"),

    path("session/<uuid:session_id>/cancel/", views.cancel_session, name="cancel_session"),
    path('FAQ', views.FAQ, name='FAQ'),

]
