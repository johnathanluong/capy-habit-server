from ninja import NinjaAPI, Schema
from typing import Optional

from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_jwt.authentication import JWTAuth
from ninja_extra import NinjaExtraAPI



api = NinjaExtraAPI()
api.register_controllers(NinjaJWTDefaultController)
api.add_router("/habits/", "habits.api.router")
api.add_router("/users/", "users.api.router")

class UserSchema(Schema):
    username: str
    display_name: str
    level: int
    points: int
    experience_points: int
    xp_for_level: int

@api.get("/me", response=UserSchema, auth=JWTAuth())
def get_user_details(request):
    return request.user
