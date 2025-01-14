from ninja import Router, Schema
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.core.cache import cache
from django.contrib.auth import authenticate
from django.db.models import Q
from ninja_jwt.tokens import RefreshToken
from ninja.errors import HttpError
import secrets

from .schemas import LoginSchema, RegisterSchema, VerifySchema

router = Router()
User = get_user_model()
    
@router.post('/register')
def register(request, data: RegisterSchema):
    # Check if password matches validation
    if data.password != data.confirmPassword:
        raise HttpError(400, 'Passwords do not match.')

    
    # Check if username or email has already been used
    if User.objects.filter(username=data.username).exists():
        raise HttpError(400, 'Username already taken')
    if User.objects.filter(email=data.email).exists():
        raise HttpError(400, 'Email already registered')
    
    # Create the new user
    newUser = User.objects.create_user(
        username=data.username,
        password=data.password,
        email=data.email,
        is_active=False,
        is_staff=False,
        is_superuser=False
    )
    
    # Add the new user to the regular_user group
    try:
        user_group = Group.objects.get(name='regular_user')
        newUser.groups.add(user_group)
    except Group.DoesNotExist:
        raise HttpError(400, 'User group does not exist')
    
    # Create a verification code for the verification for the account
    verification_token = secrets.token_urlsafe(32)
    cache.set(f"verification_token_{data.email}", verification_token, timeout=86400)

    # Send the email to the provided email address
    verification_url = f"http://localhost:3000/verify-email?token={verification_token}&email={data.email}"
    send_mail(
        subject="Verify your email address with Capy Habits!",
        message=f"Click on the link below to verify your email address:\n{verification_url}\nIf you did not register for Capy Habits, ignore this email.",
        from_email="noreply@capyhabits.com",
        recipient_list=[data.email]
    )
    
    return {"message": 'Registration successful, check your email for a verification code.'}


@router.post("/verify")
def verify_email(request, data:VerifySchema):
    # Retrieve the token and email from request body
    token = data.token
    email = data.email

    if not token:
        raise HttpError(400, 'No verification code')

    # Get the cached token for that email and compare
    stored_token = cache.get(f"verification_token_{email}")
    if not stored_token or stored_token != token:
        raise HttpError(400, 'Invalid or expired verification token')
    
    # Activate the user
    try:
        user = User.objects.get(email=email)
        user.is_active = True
        user.save()

        # Clear the verification code from cache
        cache.delete(f"verification_token_{email}")

        return {"message": "Email verified successfully."}
    except User.DoesNotExist:
        raise HttpError(404, 'User does not exist.')


@router.post("/login")
def login(request, data:LoginSchema):
    # Query the users table for the username or email
    user_query = Q(username=data.identifier) | Q(email=data.identifier)
    try:
        user = User.objects.get(user_query)
    except User.DoesNotExist:
        raise HttpError(401, 'Invalid username or email')
    
    # Try to authenticate using the user and their password
    user = authenticate(request, username=user.username, password=data.password)
    if not user:
        raise HttpError(401, 'Invalid password')
    if not user.is_active:
        raise HttpError(401, 'Account has not been activated')

    # Generate tokens
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)

    return {
        "username": user.username,
        "access": access_token,
        "refresh": refresh_token,
    }
