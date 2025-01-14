from ninja import Router
from ninja_jwt.authentication import JWTAuth
from typing import List
from django.shortcuts import get_object_or_404
from ninja.errors import HttpError

from .schemas import HabitDetailSchema, HabitCreateSchema
from .models import Habit, FREQUENCY_CHOICES

router = Router()

@router.get("", response=List[HabitDetailSchema], auth=JWTAuth())
def list_habit_entries(request):
    query = Habit.objects.filter(user=request.user)
    return query

@router.post("/create", response=HabitDetailSchema, auth=JWTAuth())
def create_habit(request, habit: HabitCreateSchema):
    habit_data = habit.dict(exclude_unset=True)
    habit_data['user'] = request.user
    
    if habit_data.get('frequency_type') not in dict(FREQUENCY_CHOICES):
        raise HttpError(404, 'Invalid frequency type')
    
    habit = Habit.objects.create(**habit_data)
    return habit 

@router.delete("/{habit_id}", auth=JWTAuth())
def delete_habit(request, habit_id: int):
    habit = get_object_or_404(Habit, id=habit_id)
    habit.delete()
    
    return {"message": "Successfully deleted habit."}

@router.put("/{habit_id}", response=HabitDetailSchema, auth=JWTAuth())
def modify_habit(request, habit_id: int, payload: HabitCreateSchema):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    habit_data = payload.dict(exclude_unset=True)
    
    for attr, value in habit_data.items():
        setattr(habit, attr, value)
    habit.save()
    
    return habit

@router.post("{habit_id}/complete", auth=JWTAuth())
def complete_habit_entry(request, habit_id: int):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    return habit

@router.post("{habit_id}/miss", auth=JWTAuth())
def miss_habit_entry(request, habit_id: int):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    return habit