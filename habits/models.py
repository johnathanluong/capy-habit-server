from django.db import models
from django.conf import settings
from datetime import timedelta

frequency_choices = [
    ('daily', 'Daily'),
    ('weekly', 'Weekly'),
    ('monthly', 'Monthly')
]

status_choices = [
    ('completed', 'Completed'),
    ('missed', 'Missed')
]

# Create your models here.
class Habit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=50, blank=True)
    
    frequency = models.PositiveIntegerField(default=1) # How frequent a user wants that habit done per frequency_type
    frequency_type = models.CharField(max_length=8, 
                                      choices=frequency_choices,
                                      default='daily')
    
    grace_period = models.PositiveIntegerField(default=0)
    streak = models.IntegerField(default=0)
    
    
    def __str__(self):
        return self.name
    
class HabitCompletion(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    completed_on = models.DateField()  # Date the habit was completed
    status = models.CharField(max_length=10, choices=status_choices, default='missed')
    notes = models.TextField(blank=True)
    
    def get_period_range(self):
        habit = self.habit
        
        if habit.frequency_type == 'daily':
            return self.completed_on, self.completed_on
        elif habit.frequency_type == 'weekly':
            start_date = self.completed_on - timedelta(days=self.completed_on.weekday())
            end_date = start_date + timedelta(days=6)
            return start_date, end_date
        elif habit.frequency_type == 'monthly':
            start_date = self.completed_on.replace(day=1)
            end_date = (start_date.replace(month=start_date.month + 1) - timedelta(days=1))
            return start_date, end_date
        
        return self.completed_on, self.completed_on
    
    def get_completed_count_in_period(self):
        habit = self.habit
        start_date, end_date = self.get_period_range()

        # Get all completions in this period
        completions = HabitCompletion.objects.filter(
            habit=habit,
            completed_on__range=[start_date, end_date],
            status='completed'
        )

        return completions.count()
    
    def is_within_grace_period(self):
        habit = self.habit
        _, period_end = self.get_period_range*()
        grace_period_end = period_end + timedelta(days=habit.grace_period)
        
        return self.completed_on <= grace_period_end
    
    def check_streak(self):
        habit = self.habit
        completed_count = self.get_completed_count_in_period()

        # Reset the streak if the habit frequency is less than the set frequency - grace period
        if self.status == 'missed' and not self.is_within_grace_period():
            habit.streak = 0
            
        # If completed enough within the period, increment the streak
        elif completed_count >= habit.frequency:
            habit.streak += 1
            
        habit.save()

    
        
    def __str__(self):
        return f"{self.habit.name} completed on {self.completed_on}"