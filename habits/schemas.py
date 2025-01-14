from ninja import Schema
from typing import Optional
from datetime import datetime

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
