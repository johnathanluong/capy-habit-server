from ninja import Schema
from pydantic import EmailStr

class UserCreateSchema(Schema):
    # Create a user
    username: str
    password: str
    email: EmailStr
    
    
class UserDetailSchema(Schema):
    # Get user data
    username: str
    email: EmailStr