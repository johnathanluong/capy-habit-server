from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # Extention of the default user model
    
    date_of_birth = models.DateField(
        null=True, 
        blank=True,
        help_text="The user's DOB")
    timezone = models.CharField(
        max_length=50,
        default='UTC',
        help_text="The timezone the user resides in")
    completed_habits = models.IntegerField(
        default=0,
        help_text="The number of completed habits a user has")
    last_login = models.DateTimeField(
        auto_now=True,
        help_text="Gets the last login for the user")
    points = models.PositiveIntegerField(
        default=0,
        help_text="The number of points a user has, obtained from completing habits and keeping up streaks")
    level = models.PositiveIntegerField(default=1)
    experience_points = models.PositiveIntegerField(default=0)
    