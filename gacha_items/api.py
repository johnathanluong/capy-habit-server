from ninja import Router
from ninja_jwt.authentication import JWTAuth
from typing import List
from django.shortcuts import get_object_or_404
from ninja.errors import HttpError
from django.core.validators import ValidationError

from .models import Accessory, UserAccessory
from .schemas import AccessoryDetailSchema, UserAccessoryDetailSchema

router = Router()
gacha_cost = 50

@router.get("", response=List[AccessoryDetailSchema], auth=JWTAuth())
def list_accessories(request):
    query = Accessory.objects.all()
    return query

@router.get("/inventory", response=List[UserAccessoryDetailSchema], auth=JWTAuth())
def get_user_inventory(request):
    query = UserAccessory.objects.filter(user=request.user)
    return query
    
@router.post('/pull', response=UserAccessoryDetailSchema, auth=JWTAuth())
def gacha_pull(request):
    user = request.user
    
    if user.points < gacha_cost:
        raise HttpError(400, 'Not enough points')
    
    user_accessory, _ = Accessory.gacha_pull(user)
    
    return user_accessory
    
    
    