from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')
def trainers(request):
    return render(request, 'trainers.html')

def workouts(request):
    return render(request, 'workouts.html')
def client_profile(request):
    return render(request, "client_profile.html")

def dashboard(request):
    return render(request, "dashboard.html")