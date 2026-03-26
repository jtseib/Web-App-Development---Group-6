from django.db import models
from django.urls import reverse # Used to generate URLs by reversing the URL patterns
import uuid
class User(models.Model):
    """Model representing a USER."""
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, help_text='User ID')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, null=True, blank=True)
    ROLE_CHOICES = [
        ('trainer', 'Trainer'),
        ('member', 'Member'),
        ('employee', 'Employee'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=100, choices=ROLE_CHOICES, null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']
    def __str__(self):
        return f'{self.last_name}, {self.first_name}, {self.user_id}'

class Trainer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    join_date = models.DateField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    certifications = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        ordering = ['user__last_name', 'user__first_name']

    def __str__(self):
        if self.user:
            return f"{self.user.first_name} {self.user.last_name}"
        return "Unassigned Trainer"


class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    join_date = models.DateField(null=True, blank=True)
    goal = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        ordering = ['user__last_name', 'user__first_name']

    def __str__(self):
        if self.user:
            return f"{self.user.first_name} {self.user.last_name}"
        return "Unassigned Member"


class GymHours(models.Model):
    date = models.DateField(null=True, blank=True)
    open_time = models.TimeField(null=True, blank=True)
    close_time = models.TimeField(null=True, blank=True)
    is_closed = models.BooleanField(default=False)
    reason = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.date} - {'Closed' if self.is_closed else 'Open'}"


class WorkoutPlan(models.Model):
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.title} for {self.member}"

class Exercise(models.Model):
    plan = models.ForeignKey(WorkoutPlan, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    reps = models.IntegerField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.name} {self.plan.title}'

class TimeSlot(models.Model):
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_available = models.BooleanField(default=True)

    class Meta:
        unique_together = ('trainer', 'start_time', 'end_time')

    def __str__(self):
        return f'{self.trainer}  |  {self.start_time} - {self.end_time}'

class WorkoutLog(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    reps = models.IntegerField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.member} - {self.exercise} on {self.date}'

class WorkoutInstance(models.Model):
    res_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, help_text='Workout ID')
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    timeslot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    status = models.CharField(max_length = 20, choices=[('confirmed', 'Confirmed'), ('pending', 'Pending'), ('canceled', 'Canceled')], default='pending')

    def __str__(self):
        return f'{self.res_id}  -  {self.member} with {self.trainer} at {self.timeslot}'

class FAQ(models.Model):
    question = models.CharField(max_length=200)
    answer = models.TextField(blank=True)

    def __str__(self):
        return f'{self.question} - {self.answer}'

class TrainingProgram(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title}'

