from django import forms
from .models import GymHours


class GymHoursForm(forms.ModelForm):
    class Meta:
        model = GymHours
        fields = '__all__'