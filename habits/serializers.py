from rest_framework import serializers
from .models import Habit

class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = ['id', 'name', 'description', 'category', 'frequency', 'frequency_type', 'streak']
        