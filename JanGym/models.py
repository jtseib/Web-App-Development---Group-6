from django.db import models
from django.urls import reverse # Used to generate URLs by reversing the URL patterns
import uuid
class Employee(models.Model):
    """Model representing an Employee."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    emp_num = models.IntegerField()
    is_trainer = models.CharField(max_length=1, choices= [('y', 'Yes'), ('n', 'No')], default='n')
    date_of_birth = models.DateField(null=True, blank=True)
    class Meta:
        ordering = ['last_name', 'first_name']
    def get_absolute_url(self):
        """Returns the URL to access a particular Employee instance."""
        return reverse('emp_detail', args=[str(self.id)])
    def __str__(self):
        return f'{self.last_name}, {self.first_name}, {self.emp_num}'


class Trainer(models.Model):
    """Model representing a Gym trainer."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    employee = models.ForeignKey('Employee',null=True, blank=True, on_delete=models.CASCADE)
    email = models.EmailField(max_length=100, null=True, blank=True)
    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        email = models.EmailField(max_length=100, null=True, blank=True)

        return reverse('trainer_detail', args=[str(self.id)])
    def __str__(self):
        """String for representing the Model object."""
        return f'{self.last_name}, {self.first_name}'

class Member(models.Model):
    """Model representing a member."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    trainer = models.ForeignKey('Trainer',  on_delete=models.RESTRICT, null=True, related_name='member')

    def __str__(self):
        """String for representing the Model object."""
        return self.first_name + ' ' + self.last_name

    def get_absolute_url(self):
        """Returns the URL to access a detail record for this book."""
        return reverse('book_detail', args=[str(self.id)])
class Reservations(models.Model):
    """Model representing a reservation of a member."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    datetime = models.DateField(null=True, blank=True)
    trainer = models.ForeignKey('Trainer', on_delete=models.RESTRICT, null=True)
    member = models.ForeignKey('Member', on_delete=models.RESTRICT, null=True)
    WORKOUT_CHOICES = [
        ('u', 'Upper-body weights'),
        ('l', 'Lower-body weights'),
        ('a', 'Aerobic'),
        ('t', 'Trainer Choice'),
    ]

    workout = models.CharField(
        max_length=1,
        choices=WORKOUT_CHOICES,
        blank=True,
        default='t',
        help_text='Workout type',
    )

    res_num = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Reservation Number')
    status = models.CharField(
        max_length=1,
        choices=[
            ('c', 'Confirmed'),
            ('n', 'No Confirmation'),
        ]
    )

    class Meta:
        ordering = ['datetime', 'res_num', 'member', 'trainer' ]

    def __str__(self):
        return f'{self.res_num} ({self.last_name} {self.datetime}) {str(self.trainer)}'
