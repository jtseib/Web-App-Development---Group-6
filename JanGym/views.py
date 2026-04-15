import calendar
from datetime import date, time
from django.contrib import messages

from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DetailView

from .forms import GymHoursForm, WorkoutLogForm, ClientProfileForm
from JanGym.models import GymHours, WorkoutPlan, Exercise, WorkoutLog


def index(request):
    return render(request, 'index.html')


@login_required
def trainers(request):
    return render(request, 'trainers.html')


@login_required
def workouts(request):
    workout_plans = WorkoutPlan.objects.filter(member=request.user).prefetch_related('exercise_set')
    workout_logs = WorkoutLog.objects.filter(member=request.user).select_related('exercise').order_by('-date')

    context = {
        'workout_plans': workout_plans,
        'workout_logs': workout_logs,
    }
    return render(request, 'workouts.html', context)
@login_required
def log_workout_progress(request):
    assigned_exercises = Exercise.objects.filter(plan__member=request.user)

    if request.method == 'POST':
        form = WorkoutLogForm(request.POST)
        form.fields['exercise'].queryset = assigned_exercises

        if form.is_valid():
            workout_log = form.save(commit=False)
            workout_log.member = request.user
            workout_log.save()
            return redirect('workouts')
    else:
        form = WorkoutLogForm()
        form.fields['exercise'].queryset = assigned_exercises

    return render(request, 'log_workout_progress.html', {'form': form})
@login_required
def client_profile(request):
    if request.method == 'POST':
        form = ClientProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Information saved successfully!")
            return redirect('client_profile')
    else:
        form = ClientProfileForm(instance=request.user)

    return render(request, 'client_profile.html', {'form': form})

def dashboard(request):
    return render(request, "dashboard.html")


def client_sessions(request):
    return render(request, 'client_sessions.html')


def cancel_session(request):
    return render(request, 'cancel_session.html')


def reschedule_session(request):
    return render(request, 'reschedule_session.html')


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
