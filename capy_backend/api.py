from ninja import NinjaAPI, Schema
from typing import Optional

from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_jwt.authentication import JWTAuth
from ninja_extra import NinjaExtraAPI



api = NinjaExtraAPI()
api.register_controllers(NinjaJWTDefaultController)
api.add_router("/habits/", "habits.api.router")

class UserSchema(Schema):
    username: str
    is_authenticated: bool
    email: Optional[str] = None

@api.get("/hello")
def hello(request):
    print(request)
    return "Hello World"

@api.get("/me", response=UserSchema, auth=JWTAuth())
def me(request):
    return request.user
