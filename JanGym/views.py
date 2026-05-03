import calendar
from datetime import date, time
import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView

from .forms import GymHoursForm
from .models import (
    GymHours,
    WorkoutInstance,
    DefaultAvailability,
    TrainerAvailability
)


def index(request):
    return render(request, 'index.html')


from django.utils import timezone

@login_required
def dashboard(request):
    user = request.user
    now = timezone.now()

    # Trainer may not exist
    trainer = getattr(user, "trainer", None)

    # Upcoming sessions based on TimeSlot start_time
    upcoming_sessions = (
        WorkoutInstance.objects
        .filter(member=user, timeslot__start_time__gte=now)
        .order_by("timeslot__start_time")
    )

    next_session = upcoming_sessions.first()

    return render(request, "dashboard.html", {
        "trainer": trainer,
        "upcoming_sessions": upcoming_sessions,
        "next_session": next_session,
    })



def client_sessions(request):
    sessions = WorkoutInstance.objects.all()
    return render(request, 'client_sessions.html', {'sessions': sessions})


def cancel_session(request):
    return render(request, 'cancel_session.html')


def reschedule_session(request):
    if request.method == 'POST':
        return redirect('client_sessions')
    return render(request, 'reschedule_session.html')


def log_workout_progress(request):
    return render(request, 'log_workout_progress.html')


@login_required
def trainers(request):
    return render(request, 'trainers.html')


@login_required
def workouts(request):
    return render(request, 'workouts.html')


@login_required
def client_profile(request):
    return render(request, 'client_profile.html')


class UpdateHours(UpdateView):
    model = GymHours
    form_class = GymHoursForm
    template_name = 'update_hours.html'
    success_url = reverse_lazy('calendar_month')


class HoursListView(ListView):
    model = GymHours
    template_name = 'gymhours_list.html'
    context_object_name = 'hours'


class MonthlyCalendarView(View):
    template_name = "calendar_month.html"

    def get(self, request, year=None, month=None):
        today = date.today()
        year = year or today.year
        month = month or today.month

        cal = calendar.Calendar(firstweekday=0)
        month_days = cal.monthdatescalendar(year, month)

        hours_by_date = {
            gh.date: gh
            for gh in GymHours.objects.filter(date__year=year, date__month=month)
        }

        context = {
            "year": year,
            "month": month,
            "month_name": calendar.month_name[month],
            "month_days": month_days,
            "hours_by_date": hours_by_date,
        }

        return render(request, self.template_name, context)


class CreateHours(CreateView):
    model = GymHours
    form_class = GymHoursForm
    template_name = 'update_hours.html'
    success_url = reverse_lazy('calendar_month')

    def get_initial(self):
        return {
            'date': date(self.kwargs['year'], self.kwargs['month'], self.kwargs['day']),
            'open_time': time(5, 0),
            'close_time': time(23, 0),
        }


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})


def trainer_dashboard(request):
    today = datetime.date.today()
    now = datetime.datetime.now().time()

    # Get the next availability block
    next_availability = (
        TrainerAvailability.objects
        .filter(
            trainer=request.user,
            date__gte=today
        )
        .order_by("date", "start_time")
        .first()
    )

    context = {
        "next_availability": next_availability
    }

    return render(request, 'trainer_dashboard.html', context)



# ---------------------------------------------------------
# TRAINER CALENDAR (FULLY FIXED)
# ---------------------------------------------------------

def trainer_calendar(request, year=None, week=None):
    today = datetime.date.today()

    # Determine the week to display
    if year is None or week is None:
        today = datetime.date.today()
        return redirect("trainer_calendar_week", year=today.year, week=today.isocalendar().week)

        year = today.year
        month = today.month
        week = today.isocalendar().week

    # Get the Monday of the requested week
    monday = datetime.date.fromisocalendar(year, week, 1)
    week_days = [monday + datetime.timedelta(days=i) for i in range(7)]

    # Load custom availability for the week
    availability = TrainerAvailability.objects.filter(
        trainer=request.user,
        date__range=[week_days[0], week_days[-1]]
    )

    # Group availability by date
    availability_by_date = {}
    for a in availability:
        key = a.date.strftime("%Y-%m-%d")
        availability_by_date.setdefault(key, []).append(a)

    # Load default weekly availability
    default_availability = DefaultAvailability.objects.filter(trainer=request.user)
    default_by_weekday = {d.weekday: d for d in default_availability}

    # Time slots (6 AM → 10 PM)
    time_slots = [datetime.time(h, 0) for h in range(6, 22)]

    context = {
        "week_days": week_days,
        "availability_by_date": availability_by_date,
        "default_by_weekday": default_by_weekday,
        "time_slots": time_slots,
        "year": year,
        "week": week,
    }

    return render(request, "trainer_calendar.html", context)




# ---------------------------------------------------------
# TRAINER AVAILABILITY FORMS
# ---------------------------------------------------------

def add_availability(request):
    if request.method == "POST":
        date_str = request.POST.get("date")
        start = request.POST.get("start_time")
        end = request.POST.get("end_time")

        # Convert to Python objects
        date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        start_obj = datetime.datetime.strptime(start, "%H:%M").time()
        end_obj = datetime.datetime.strptime(end, "%H:%M").time()

        # Convert to datetime for iteration
        dt_start = datetime.datetime.combine(date_obj, start_obj)
        dt_end = datetime.datetime.combine(date_obj, end_obj)

        # Generate 30-minute increments
        current = dt_start
        while current < dt_end:
            next_slot = current + datetime.timedelta(minutes=30)

            TrainerAvailability.objects.create(
                trainer=request.user,
                date=date_obj,
                start_time=current.time(),
                end_time=next_slot.time()
            )

            current = next_slot

        return redirect("trainer_calendar")

    return render(request, "add_availability.html")



def set_default_availability(request):
    if request.method == "POST":
        days = request.POST.getlist("days")  # list of weekday numbers
        start = request.POST.get("start_time")
        end = request.POST.get("end_time")

        start_obj = datetime.datetime.strptime(start, "%H:%M").time()
        end_obj = datetime.datetime.strptime(end, "%H:%M").time()

        for weekday in days:
            weekday = int(weekday)

            # Find next occurrence of this weekday
            today = datetime.date.today()
            days_ahead = (weekday - today.weekday()) % 7
            target_date = today + datetime.timedelta(days=days_ahead)

            # Convert to datetime for iteration
            dt_start = datetime.datetime.combine(target_date, start_obj)
            dt_end = datetime.datetime.combine(target_date, end_obj)

            # Generate 1-hour increments
            current = dt_start
            while current < dt_end:
                next_slot = current + datetime.timedelta(hours=1)

                TrainerAvailability.objects.create(
                    trainer=request.user,
                    date=target_date,
                    start_time=current.time(),
                    end_time=next_slot.time()
                )

                current = next_slot

        return redirect("trainer_calendar")

    return render(request, "set_default_availability.html")




def trainer_availability(request):
    return render(request, 'trainer_availability.html')


def available_sessions(request):
    return render(request, 'available_sessions.html')

def client_available_sessions(request, year=None, week=None):
    profile = request.user.memberprofile
    trainer = profile.trainer

    if trainer is None:
        return render(request, "no_trainer.html")

    # Only show THIS trainer's availability
    availability = TrainerAvailability.objects.filter(
        trainer=trainer,
        date__range=[week_days[0], week_days[-1]]
    ).order_by("date", "start_time")


def book_session(request, slot_id):
    slot = TrainerAvailability.objects.get(id=slot_id)

    # Create workout instance
    WorkoutInstance.objects.create(
        trainer=slot.trainer,
        member=request.user,
        timeslot_start=slot.start_time,
        timeslot_end=slot.end_time,
        date=slot.date
    )


    slot.delete()

    return redirect("client_sessions")


