from django.contrib import admin

# Register your models here.
from .models import Habit, HabitCompletion

admin.site.register(Habit)
admin.site.register(HabitCompletion)