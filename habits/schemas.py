from ninja import Schema
from typing import Optional, Dict
from datetime import datetime
from .models import HabitCompletion

class HabitCreateSchema(Schema):
    name: str
    description: str
    category: Optional[str] = None
    frequency: int = 1
    frequency_type: str = 'daily'
    grace_period: int = 0

class HabitDetailSchema(Schema):
    id: int
    name: str
    description: str
    category: Optional[str]
    frequency: int
    frequency_type: str
    grace_period: int
    streak: int
    created: datetime
    modified: datetime
    progress: dict
    capybara_stack: dict
    accessory: Optional[Dict] = None

    # progress { completed, required }
    @staticmethod
    def resolve_progress(obj):
        start, end = obj.current_period_range()
        completed = HabitCompletion.objects.filter(
            habit=obj,
            completed_at__range=[start, end],
            status='completed'
        ).count()
        return {
            "completed": completed,
            "required": obj.frequency
        }
    
    # capybara_stack { small, medium, large }
    @staticmethod
    def resolve_capybara_stack(obj):
        return obj.capybara_stack
    
    @staticmethod
    def resolve_accessory(obj):
        try:
            if not obj.accessory:
                return None
                
            return {
                "id": obj.accessory.id,
                "name": obj.accessory.name,
                "description": obj.accessory.description,
                "image_filename": obj.accessory.image_filename,
                "rarity": obj.accessory.rarity
            }
        except Exception as e:
            print(f"Debug - Accessory resolution error: {str(e)}")
            return None
    

class AccessorizeSchema(Schema):
    accessory_id: int
