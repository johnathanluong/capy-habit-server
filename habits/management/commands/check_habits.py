from django.core.management.base import BaseCommand
from django.utils import timezone
from habits.models import Habit

class Command(BaseCommand):
    help = 'Checks all habits and marks missed ones'

    def handle(self, *args, **options):
        habits = Habit.objects.all()
        checked = 0
        missed = 0

        for habit in habits:
            if habit.check_period_completion():
                missed += 1
            checked += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Checked {checked} habits, marked {missed} as missed'
            )
        )