from ninja import Schema
from datetime import datetime

class HabitCreateSchema(Schema):
    # Create a habit
    name: str
    description: str
    frequency: int
    
class HabitDetailSchema(Schema):
    # Get habit data
    id: int
    name: str
    description: str
    frequency: int
    created: datetime
    modified: datetime