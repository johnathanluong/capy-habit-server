from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta, datetime
from calendar import monthrange
from django.core.validators import ValidationError
import pytz

FREQUENCY_CHOICES = [
    ('daily', 'Daily'),    # Habit should be completed daily
    ('weekly', 'Weekly'),  # Habit should be completed weekly
    ('monthly', 'Monthly'), # Habit should be completed monthly
]

STATUS_CHOICES = [
    ('completed', 'Completed'),  # Habit was completed successfully
    ('missed', 'Missed'),       # Habit was not completed in time
]

class Habit(models.Model):
    # Model for each habit
    
    # Main fields
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        help_text="The user who owns this habit"
    )
    name = models.CharField(
        max_length=255,
        help_text="The name of the habit"
    )
    description = models.TextField(
        help_text="Detailed description of the habit"
    )
    category = models.CharField(
        max_length=50,
        blank=True,
        help_text="Optional category for organizing habits"
    )
    created = models.DateTimeField(
        editable=False,
        default=timezone.now
    )
    modified = models.DateTimeField(
        auto_now=True
    )
    
    # Frequency settings
    frequency = models.PositiveIntegerField(
        default=1,
        help_text="How many times the habit should be completed per frequency_type"
    )
    frequency_type = models.CharField(
        max_length=8,
        choices=FREQUENCY_CHOICES,
        default='daily',
        help_text="The time period over which the frequency is measured"
    )
    
    # Tracking fields
    grace_period = models.PositiveIntegerField(
        default=0,
        help_text="Number of days after the period ends where completion still counts"
    )
    streak = models.IntegerField(
        default=0,
        help_text="Current streak of successful completions"
    )
    
    def get_user_timezone(self):
        return pytz.timezone(self.user.timezone)


    def get_user_local_time(self, dt=None):
        if dt is None:
            dt = timezone.now()
        return dt.astimezone(self.get_user_timezone())
    
    
    def get_period_completions(self):
        start, end = self.current_period_range()
        return HabitCompletion.objects.filter(
            habit=self,
            completed_at__range=[start, end],
            status='completed'
        ).count()
    
    
    # Get current period range for checking if habit has enough completions
    def current_period_range(self):
        local_dt = self.get_user_local_time()
        user_tz = self.get_user_timezone()
        
        if self.frequency_type == 'daily':
            start = datetime.combine(local_dt.date(), datetime.min.time())
            end = datetime.combine(local_dt.date(), datetime.max.time())
        elif self.frequency_type == 'weekly':
            start = datetime.combine(
                local_dt.date() - timedelta(days=local_dt.weekday()),
                datetime.min.time()
            )
            end = datetime.combine(
                start.date() + timedelta(days=6),
                datetime.max.time()
            )
        elif self.frequency_type == 'monthly':
            start = datetime.combine(
                local_dt.replace(day=1).date(),
                datetime.min.time()
            )
            _, last_day = monthrange(local_dt.year, local_dt.month)
            end = datetime.combine(
                local_dt.replace(day=last_day).date(),
                datetime.max.time()
            )
        
        # Localize to user timezone before converting to UTC
        start = user_tz.localize(start).astimezone(pytz.UTC)
        end = user_tz.localize(end).astimezone(pytz.UTC)
        return start, end
    
    
    # Checks if habit was completed enough times for their time period
    def check_period_completion(self):
        completed_count = self.get_period_completions()
        
        if completed_count < self.frequency:
            HabitCompletion.objects.create(
                habit=self,
                user=self.user,
                status='missed',
                completed_at=timezone.now()
            )
            self.streak = 0
            self.save()
            return True
        return False
    
    
    def increment_streak(self):
        completed_count = self.get_period_completions()
        if completed_count >= self.frequency:
            self.streak += 1
            self.save()
    
    
    def __str__(self):
        return self.name

class HabitCompletion(models.Model):
    # Model of a single habit completion
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        help_text="The user who completed the habit"
    )
    habit = models.ForeignKey(
        Habit,
        on_delete=models.CASCADE,
        help_text="The habit this completion relates to"
    )
    completed_at = models.DateTimeField(
        blank=True,
        null=True,
        help_text="The UTC datetime when the habit was completed"
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='completed',
    )
    
    # Optimizes database queries for habit, completed_at, and status
    class Meta:
        indexes = [
            models.Index(fields=['habit', 'completed_at', 'status']),
        ]
    
    @property
    # Get the completion datetime in user's timezone.
    def completed_on_local(self):
        return self.completed_at.astimezone(self.habit.get_user_timezone())
    
    # Calculate period range in user's local timezone.
    def get_period_range(self):
        local_dt = self.completed_on_local
        user_tz = self.habit.get_user_timezone()
        
        if self.habit.frequency_type == 'daily':
            # Start and end of day in user's timezone
            start = datetime.combine(local_dt.date(), datetime.min.time())
            end = datetime.combine(local_dt.date(), datetime.max.time())
            
        elif self.habit.frequency_type == 'weekly':
            # Start of week (Monday) and end of week (Sunday) in user's timezone
            start = datetime.combine(
                local_dt.date() - timedelta(days=local_dt.weekday()),
                datetime.min.time()
            )
            end = datetime.combine(
                start.date() + timedelta(days=6),
                datetime.max.time()
            )
            
        elif self.habit.frequency_type == 'monthly':
            # Start and end of month in user's timezone
            start = datetime.combine(
                local_dt.replace(day=1).date(),
                datetime.min.time()
            )
            _, last_day = monthrange(local_dt.year, local_dt.month)
            end = datetime.combine(
                local_dt.replace(day=last_day).date(),
                datetime.max.time()
            )
        
        # Localize to user's timezone and convert to UTC for database queries
        start = user_tz.localize(start).astimezone(pytz.UTC)
        end = user_tz.localize(end).astimezone(pytz.UTC)
        
        return start, end
    
    # Count completions in current period using UTC times.
    def get_completed_count_in_period(self):
        start_date, end_date = self.get_period_range()
        return HabitCompletion.objects.filter(
            habit=self.habit,
            completed_at__range=[start_date, end_date],
            status='completed'
        ).count()
    
    # Check if completion is within grace period using UTC times.
    def is_within_grace_period(self):
        _, period_end = self.get_period_range()
        grace_period_end = period_end + timedelta(days=self.habit.grace_period)
        return self.completed_at <= grace_period_end
    
    # Update streak based on local timezone periods.
    def check_streak(self):
        completed_count = self.get_completed_count_in_period()
        
        if self.status == 'missed' and not self.is_within_grace_period():
            self.habit.streak = 0
        elif completed_count >= self.habit.frequency:
            self.habit.streak += 1
        
        self.habit.save()
    
    # Save completion and update streak.
    def save(self, *args, **kwargs):
        if not self.completed_at:
            self.completed_at = timezone.now()
            
        if self.status == 'completed':
            completed_count = self.habit.get_period_completions()
            if completed_count >= self.habit.frequency:
                raise ValidationError("Maximum completions reached for this period")
            
        super().save(*args, **kwargs)
        
        if self.status == 'completed':
            self.habit.increment_streak()
    
    def __str__(self):
        local_time = self.completed_on_local
        return f"{self.habit.name} completed on {local_time.strftime('%Y-%m-%d %H:%M %Z')}"

