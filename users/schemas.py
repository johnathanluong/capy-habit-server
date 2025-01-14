from ninja import Schema
from pydantic import EmailStr

class LoginSchema(Schema):
    identifier: str
    password: str
    
class RegisterSchema(Schema):
    username: str
    email: str
    password: str
    confirmPassword: str
    
class VerifySchema(Schema):
    email: str
    token: str