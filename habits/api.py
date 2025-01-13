from ninja import Router
from ninja_jwt.authentication import JWTAuth
from typing import List
from django.shortcuts import get_object_or_404

from .schemas import HabitDetailSchema
from .schemas import HabitDetailSchema
from .models import Habit

router = Router()

@router.get("", response=List[HabitDetailSchema], auth=JWTAuth())
def list_habit_entries(request):
    query = Habit.objects.all()
    return query

@router.get("{entry_id}/", response=HabitDetailSchema, auth=JWTAuth())
def get_habit_entry(request, entry_id: int):
    obj = get_object_or_404(Habit, id=entry_id)
    return obj