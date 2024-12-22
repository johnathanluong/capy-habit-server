from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    timezone = models.CharField(max_length=50, default='UTC')
    completed_habits = models.IntegerField(default=0)
    habit_streak = models.IntegerField(default=0)
    last_login = models.DateTimeField(auto_now=True)
    points = models.PositiveIntegerField(default=0)
    
    