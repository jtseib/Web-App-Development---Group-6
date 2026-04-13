import calendar
from datetime import date, time
from django.views import View

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse

from django.views.generic import ListView, CreateView, UpdateView, DetailView
from .forms import GymHoursForm





from JanGym.models import GymHours


def index(request):
    return render(request, 'index.html')


@login_required
def trainers(request):
    return render(request, 'trainers.html')


@login_required
def workouts(request):
    return render(request, 'workouts.html')


@login_required
def client_profile(request):
    return render(request, 'client_profile.html')


def dashboard(request):
<<<<<<< HEAD
    return render(request, "dashboard.html")
def client_sessions(request):
    return render(request, 'client_sessions.html')
def cancel_session(request):
    return render(request, 'cancel_session.html')

def reschedule_session(request):
    return render(request, 'reschedule_session.html')
from django.shortcuts import render


def cancel_session(request):
    return render(request, 'cancel_session.html')


def reschedule_session(request):
    return render(request, 'reschedule_session.html')
=======
    return render(request, 'dashboard.html')

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

        # Build calendar matrix (weeks → days)
        cal = calendar.Calendar(firstweekday=0)
        month_days = cal.monthdatescalendar(year, month)

        # Fetch GymHours indexed by actual date
        hours_by_date = {
            gh.date: gh
            for gh in GymHours.objects.filter(date__year=year, date__month=month)
        }

        context = {
            "year": year,
            "month": month,
            "month_name": calendar.month_name[month],
            "month_days": month_days,
            "hours_by_date": hours_by_date,   # <-- REQUIRED
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
def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['get_hours'] = lambda d: hours_by_date.get(d)
    return context

>>>>>>> b4ee3c88254200d3b19e97a74fc227801d81f4b1
