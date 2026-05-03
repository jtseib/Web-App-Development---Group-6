from django import forms
from .models import GymHours, WorkoutLog
from django.contrib.auth.models import User

class GymHoursForm(forms.ModelForm):
    class Meta:
        model = GymHours
        fields = ['date', 'open_time', 'close_time', 'is_closed', 'reason']

        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),

            'open_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control'
            }),

            'close_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control'
            }),

            'reason': forms.TextInput(attrs={
                'class': 'form-control'
            })
        }
class WorkoutLogForm(forms.ModelForm):
    class Meta:
        model = WorkoutLog
        fields = ['exercise', 'reps', 'weight', 'duration', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }
class ClientProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]

        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }


class TrainerSelectForm(forms.Form):
    trainer = forms.ModelChoiceField(
        queryset=User.objects.filter(is_staff=True),
        required=True,
        label="Choose Your Trainer",
        widget=forms.Select(attrs={"class": "form-control"})
    )
