import calendar
from datetime import date, time
import datetime
import datetime
from django.shortcuts import render
from django.utils.timezone import now

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView
from .models import WorkoutInstance, MemberProfile
from django.db.models import F, ExpressionWrapper, DateTimeField, TimeField, DateField
from django.db.models.functions import Cast
from .forms import GymHoursForm, UserUpdateForm, TrainerSelectForm
from .models import (
    GymHours,
    WorkoutInstance,
    DefaultAvailability,
    TrainerAvailability, TimeSlot
)


def index(request):
    return render(request, 'index.html')





from django.utils import timezone

def dashboard(request):
    user = request.user

    # Member profile
    profile = user.memberprofile
    trainer = profile.trainer if profile else None

    # Current datetime (timezone-aware)
    now = timezone.now()

    # Only sessions in the future (not earlier today)
    upcoming_sessions = (
        WorkoutInstance.objects
        .filter(
            member=user,
            timeslot__start_time__gte=now
        )
        .order_by("timeslot__start_time")
    )

    # First upcoming session
    next_session = upcoming_sessions.first() if upcoming_sessions else None

    # Current week for "View Trainer Availability"
    current_year = now.year
    current_week = now.isocalendar().week

    context = {
        "trainer": trainer,
        "next_session": next_session,
        "upcoming_sessions": upcoming_sessions,
        "current_year": current_year,
        "current_week": current_week,
    }

    return render(request, "dashboard.html", context)

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
    user = request.user

    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully.")
            return redirect("client_profile")
    else:
        form = UserUpdateForm(instance=user)

    return render(request, "client_profile.html", {
        "form": form,})


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


from django.utils import timezone
import datetime

def trainer_dashboard(request):
    user = request.user
    now = timezone.now()

    # --- Upcoming booked sessions ---
    upcoming_sessions = (
        WorkoutInstance.objects
        .filter(trainer=user, timeslot__start_time__gte=now)
        .order_by("timeslot__start_time")
    )
    next_session = upcoming_sessions.first() if upcoming_sessions else None

    # --- Trainer's next availability (Python-side filtering) ---
    future_availability = []
    for slot in TrainerAvailability.objects.filter(trainer=user).order_by("date", "start_time"):
        start_dt = timezone.make_aware(
            datetime.datetime.combine(slot.date, slot.start_time),
            timezone.get_current_timezone()
        )
        if start_dt >= now:
            future_availability.append((start_dt, slot))

    next_availability = future_availability[0][1] if future_availability else None

    # --- Clients assigned to this trainer ---
    clients = (
        MemberProfile.objects
        .filter(trainer=user)
        .values("user__username", "user__id")
    )

    context = {
        "upcoming_sessions": upcoming_sessions,
        "next_session": next_session,
        "next_availability": next_availability,
        "clients": clients,
    }

    return render(request, "trainer_dashboard.html", context)



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

from datetime import date, timedelta
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import MemberProfile, TrainerAvailability


def client_available_sessions(request, year=None, week=None):
    user = request.user

    # --- 1. Handle missing MemberProfile safely ---
    try:
        profile = user.memberprofile
    except MemberProfile.DoesNotExist:
        messages.error(request, "You must complete your profile before viewing available sessions.")
        return redirect("dashboard")  # or wherever you want them to go

    # --- 2. Ensure the client has a trainer assigned ---
    trainer = profile.trainer
    if trainer is None:
        return render(request, "no_trainer.html")

    # --- 3. Determine the correct week ---
    today = date.today()

    if year is None or week is None:
        year = today.year
        week = today.isocalendar().week

    # Monday of the requested week
    week_start = date.fromisocalendar(year, week, 1)
    week_days = [week_start + timedelta(days=i) for i in range(7)]

    # --- 4. Query availability for THIS trainer only ---
    availability = TrainerAvailability.objects.filter(
        trainer=trainer,
        date__range=[week_days[0], week_days[-1]]
    ).order_by("date", "start_time")

    # --- 5. Render template ---
    return render(request, "client_available_sessions.html", {
        "trainer": trainer,
        "availability": availability,
        "week_days": week_days,
        "year": year,
        "week": week,
    })



import datetime

from django.utils.timezone import make_aware
import datetime

from django.utils import timezone
import datetime
from django.shortcuts import get_object_or_404, redirect

def book_session(request, timeslot_id):
    user = request.user

    slot = get_object_or_404(TrainerAvailability, pk=timeslot_id)

    # Convert date + time into timezone-aware datetimes using local timezone
    local_tz = timezone.get_current_timezone()

    start_dt = timezone.make_aware(
        datetime.datetime.combine(slot.date, slot.start_time),
        local_tz
    )

    end_dt = timezone.make_aware(
        datetime.datetime.combine(slot.date, slot.end_time),
        local_tz
    )

    # Create or reuse a TimeSlot
    ts, created = TimeSlot.objects.get_or_create(
        trainer=slot.trainer,
        start_time=start_dt,
        end_time=end_dt,
        defaults={"is_available": False},
    )

    # If it already existed, mark unavailable
    if not created:
        ts.is_available = False
        ts.save()

    # Create the workout session
    WorkoutInstance.objects.create(
        member=user,
        trainer=slot.trainer,
        timeslot=ts,
        status="confirmed"
    )

    # Remove the availability slot so it cannot be double-booked
    slot.delete()

    return redirect("dashboard")

def select_trainer(request):
    user = request.user

    # Ensure profile exists
    try:
        profile = user.memberprofile
    except MemberProfile.DoesNotExist:
        messages.error(request, "You must complete your profile first.")
        return redirect("dashboard")

    if request.method == "POST":
        form = TrainerSelectForm(request.POST)
        if form.is_valid():
            profile.trainer = form.cleaned_data["trainer"]
            profile.save()
            messages.success(request, "Trainer selected successfully.")
            return redirect("dashboard")
    else:
        form = TrainerSelectForm()

    return render(request, "select_trainer.html", {"form": form})

def trainer_available_sessions(request):
    user = request.user

    # Ensure member profile exists
    try:
        profile = user.memberprofile
    except MemberProfile.DoesNotExist:
        messages.error(request, "You must complete your profile first.")
        return redirect("dashboard")

    trainer = profile.trainer
    if not trainer:
        return render(request, "error.html", {"message": "You do not have a trainer assigned."})

    # Load future availability
    available_slots = (
        TrainerAvailability.objects
        .filter(
            trainer=trainer,
            date__gte=timezone.now().date()
        )
        .order_by("date", "start_time")
    )

    return render(request, "trainer_available_sessions.html", {
        "trainer": trainer,
        "available_slots": available_slots,
    })

from django.utils.timezone import make_aware

def book_trainer_slot(request, slot_id):
    slot = get_object_or_404(TrainerAvailability, id=slot_id)

    # GET → show confirmation page
    if request.method == "GET":
        return render(request, "book_session.html", {"slot": slot})

    # POST → convert TrainerAvailability → TimeSlot
    if request.method == "POST":
        user = request.user

        # Combine date + time into timezone-aware datetimes
        start_dt = make_aware(datetime.datetime.combine(slot.date, slot.start_time))
        end_dt = make_aware(datetime.datetime.combine(slot.date, slot.end_time))

        # Create or reuse a TimeSlot
        ts, created = TimeSlot.objects.get_or_create(
            trainer=slot.trainer,
            start_time=start_dt,
            end_time=end_dt,
            defaults={"is_available": False},
        )

        # Mark the slot unavailable if it was reused
        if not created:
            ts.is_available = False
            ts.save()

        # Create the WorkoutInstance
        WorkoutInstance.objects.create(
            member=user,
            trainer=slot.trainer,
            timeslot=ts,
            status="confirmed",
        )

        return redirect("dashboard")


def trainer_available_calendar(request, year=None, week=None):
    user = request.user

    # Ensure member profile exists
    try:
        profile = user.memberprofile
    except MemberProfile.DoesNotExist:
        return render(request, "error.html", {"message": "No member profile found."})

    trainer = profile.trainer
    if not trainer:
        return render(request, "error.html", {"message": "You do not have a trainer assigned."})

    # Determine the week to display
    today = datetime.date.today()
    if year is None or week is None:
        return redirect(
            "trainer_available_calendar",
            year=today.year,
            week=today.isocalendar().week
        )

    # Get Monday of the requested week
    monday = datetime.date.fromisocalendar(year, week, 1)
    week_days = [monday + datetime.timedelta(days=i) for i in range(7)]

    # Load availability for THIS trainer for the week
    availability = TrainerAvailability.objects.filter(
        trainer=trainer,
        date__range=[week_days[0], week_days[-1]]
    ).order_by("date", "start_time")

    # Group availability by date (same as trainer calendar)
    availability_by_date = {}
    for a in availability:
        key = a.date.strftime("%Y-%m-%d")
        availability_by_date.setdefault(key, []).append(a)

    # Time slots (6 AM → 10 PM) — same as trainer calendar
    time_slots = [datetime.time(h, 0) for h in range(6, 22)]

    context = {
        "trainer": trainer,
        "week_days": week_days,
        "availability_by_date": availability_by_date,
        "time_slots": time_slots,
        "year": year,
        "week": week,
    }

    return render(request, "trainer_available_calendar.html", context)

def trainer_view_client(request, user_id):
    trainer = request.user

    # Make sure the trainer is allowed to view this client
    client_profile = get_object_or_404(MemberProfile, user__id=user_id, trainer=trainer)

    context = {
        "client": client_profile,
        "client_user": client_profile.user,
    }

    return render(request, "trainer_view_client.html", context)

