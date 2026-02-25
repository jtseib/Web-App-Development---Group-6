from django.contrib import admin
from .models import Employee, Trainer, Member, Reservations
# Register your models here.
admin.site.register(Employee)
admin.site.register(Trainer)
admin.site.register(Member)
admin.site.register(Reservations)
