from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


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
    return render(request, "client_profile.html")

def dashboard(request):
    return render(request, "dashboard.html")