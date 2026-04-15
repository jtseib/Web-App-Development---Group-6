from django import forms
from .models import GymHours

<<<<<<< HEAD

class GymHoursForm(forms.ModelForm):
    class Meta:
        model = GymHours
        fields = '__all__'
=======
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
>>>>>>> caec5d440b03c99a3049fa4a7ad58b370980d1ce
