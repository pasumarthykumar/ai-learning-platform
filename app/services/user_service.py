from passlib.context import CryptContext
from models import UserCreate
from repositories.user_repository import insert_user, find_user_by_email
import jwt
from fastapi import HTTPException
from decouple import config

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = config("SECRET_KEY")  # Replace with a secure key
ALGORITHM = "HS256"

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

async def create_user(user: UserCreate):
    
    # Convert UserCreate model to dictionary
    user_dict = dict(user)

    # Hash the password
    user_dict["hashed_password"] = hash_password(user.password)
    del user_dict["password"]  # Remove the plain password

    # Check if a user already exists with the same email
    existing_user = await find_user_by_email(user.email)
    if existing_user:
        raise ValueError("User with this email already exists")

    # Insert the new user into the database
    await insert_user(user_dict)
    return user_dict

async def authenticate_user(email: str, password: str):
    user = await find_user_by_email(email)
    if not user:
        return None
    if not pwd_context.verify(password, user.hashed_password):
        return None
    return user

def create_access_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
