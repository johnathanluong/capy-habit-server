from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # Extention of the default user model
    email = models.EmailField(unique=True)
    display_name = models.CharField(
        max_length=100,
        default=''
        )
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
    
    def __str__(self):
        return f"Username: {self.username}, Display Name: {self.display_name}"
    