from django.contrib import admin
from .models import User, Trainer, Member, GymHours, WorkoutPlan, Exercise, TimeSlot, WorkoutLog, WorkoutInstance, FAQ, TrainingProgram
# Register your models here.
admin.site.register(User)
admin.site.register(Trainer)
admin.site.register(Member)
admin.site.register(GymHours)
admin.site.register(WorkoutPlan)
admin.site.register(Exercise)
admin.site.register(TimeSlot)
admin.site.register(WorkoutLog)
admin.site.register(WorkoutInstance)
admin.site.register(FAQ)
admin.site.register(TrainingProgram)





