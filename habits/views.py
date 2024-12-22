from rest_framework import viewsets
from .models import Habit
from .serializers import HabitSerializer

class HabitViewSet(viewsets.ModelViewSet):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
