from ninja import Schema
from typing import Dict, Union

class AccessoryDetailSchema(Schema):
    id: int
    name: str
    description: str
    image_filename: str
    rarity: str
    
class UserAccessoryDetailSchema(Schema):
    accessory: Dict[str, Union[int, str]]
    quantity: int
    number_used: int
    
    # accessory: {name, description, image_filename, rarity}
    @staticmethod
    def resolve_accessory(obj):
        return {
            "id": obj.accessory.id,
            "name": obj.accessory.name,
            "description": obj.accessory.description,
            "image_filename": obj.accessory.image_filename,
            "rarity": obj.accessory.rarity
        }
