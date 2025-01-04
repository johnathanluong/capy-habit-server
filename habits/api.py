from ninja import Router
from typing import List
from django.shortcuts import get_object_or_404
from .schemas import HabitDetailSchema
from .schemas import HabitDetailSchema
from .models import Habit

router = Router()

@router.get("", response=List[HabitDetailSchema])
def list_habit_entries(request):
    query = Habit.objects.all()
    return query

@router.get("{entry_id}/", response=HabitDetailSchema)
def get_habit_entry(request, entry_id: int):
    obj = get_object_or_404(Habit, id=entry_id)
    return obj