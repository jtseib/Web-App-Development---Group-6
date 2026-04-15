from django.db import models
from django.contrib.auth.models import User
import uuid


class GymHours(models.Model):
    date = models.DateField(null=True, blank=True)
    open_time = models.TimeField(null=True, blank=True)
    close_time = models.TimeField(null=True, blank=True)
    is_closed = models.BooleanField(default=False)
    reason = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name = "Gym Hour"
        verbose_name_plural = "Gym Hours"
    def __str__(self):
        status = "Closed" if self.is_closed else "Open"
        return f"{self.date} - {status}"


class WorkoutPlan(models.Model):
    trainer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="trainer_plans")
    member = models.ForeignKey(User, on_delete=models.CASCADE, related_name="member_plans")
    title = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.title} ({self.member.username})"


class Exercise(models.Model):
    plan = models.ForeignKey(WorkoutPlan, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    reps = models.IntegerField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.plan.title})"


class TimeSlot(models.Model):
    trainer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="trainer_timeslots")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_available = models.BooleanField(default=True)

    class Meta:
        unique_together = ('trainer', 'start_time', 'end_time')

    def __str__(self):
        return f"{self.trainer.username} | {self.start_time} - {self.end_time}"


class WorkoutLog(models.Model):
    member = models.ForeignKey(User, on_delete=models.CASCADE, related_name="member_logs")
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    reps = models.IntegerField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.member.username} - {self.exercise.name} on {self.date}"


class WorkoutInstance(models.Model):
    res_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    member = models.ForeignKey(User, on_delete=models.CASCADE, related_name="member_workouts")
    trainer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="trainer_workouts")
    timeslot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=[
            ('confirmed', 'Confirmed'),
            ('pending', 'Pending'),
            ('canceled', 'Canceled')
        ],
        default='pending'
    )

    def __str__(self):
        return f"{self.res_id} - {self.member.username} with {self.trainer.username}"


class FAQ(models.Model):
    question = models.CharField(max_length=200)
    answer = models.TextField(blank=True)

    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

    def __str__(self):
        return self.question


class TrainingProgram(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    trainer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="trainer_programs")

    def __str__(self):
        return self.title
