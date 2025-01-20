from ninja import Router
from ninja_jwt.authentication import JWTAuth
from typing import List
from django.shortcuts import get_object_or_404
from ninja.errors import HttpError
from django.core.validators import ValidationError

from .schemas import HabitDetailSchema, HabitCreateSchema, AccessorizeSchema
from .models import Habit, HabitCompletion, FREQUENCY_CHOICES
from gacha_items.models import UserAccessory

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
    try:
        habit = get_object_or_404(Habit, id=habit_id, user=request.user)
        completion = HabitCompletion.objects.create(
            user=request.user,
            habit=habit,
            status='completed'
        )
        
        start, end = habit.current_period_range()
        completed_count = HabitCompletion.objects.filter(
            habit=habit,
            completed_at__range=[start, end],
            status='completed'
        ).count()
        
        request.user.completeHabit()
        request.user.save()
        
        return {"success": True, "completion_id": completion.id, "progress": completed_count, "required": habit.frequency}
    except ValidationError as e:
        raise HttpError(400, str(e))


@router.post("{habit_id}/accessory", auth=JWTAuth())
def accessorize_habit_entry(request, habit_id: int, payload: AccessorizeSchema):
    try:
        # Get habit and verify ownership
        habit = get_object_or_404(Habit, id=habit_id, user=request.user)
        
        # Removes the accesory if the payload == -1
        if payload.accessory_id == -1:
            if habit.accessory:
                old_user_accessory = get_object_or_404(
                    UserAccessory,
                    user=request.user,
                    accessory=habit.accessory
                )
                old_user_accessory.stop_using_accessory(1)
                habit.accessory = None
                habit.save()
                return {
                    "success": True,
                    "habit_id": habit.id,
                    "accessory": None
                }
            return {
                "success": True,
                "habit_id": habit.id,
                "accessory": None
            }
        
        # Get user's accessory and verify ownership
        user_accessory = get_object_or_404(
            UserAccessory, 
            user=request.user,
            accessory_id=payload.accessory_id
        )
        
        # Check if accessory is available (not all copies are in use)
        if user_accessory.quantity <= user_accessory.number_used:
            raise HttpError(400, "All copies of this accessory are in use")
            
        # If habit already has an accessory, release it
        if habit.accessory:
            old_user_accessory = get_object_or_404(
                UserAccessory,
                user=request.user,
                accessory=habit.accessory
            )
            old_user_accessory.stop_using_accessory(1)
            
        # Assign new accessory
        habit.accessory = user_accessory.accessory
        habit.save()
        
        # Mark accessory as in use
        user_accessory.use_accessory(1)
        
        return {
            "success": True,
            "habit_id": habit.id,
            "accessory": {
                "id": user_accessory.accessory.id,
                "name": user_accessory.accessory.name
            }
        }
        
    except ValidationError as e:
        raise HttpError(400, str(e))