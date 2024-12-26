from fastapi import FastAPI, HTTPException, APIRouter
from models import UserCreate
from models import LoginRequest
from services.user_service import create_user
from services.user_service import authenticate_user, create_access_token

auth_router = APIRouter()

@auth_router.post("/auth/register")
async def register_user(user: UserCreate):
    try:
        await create_user(user)
        print("Register endpoint hit")
        return {"message": "User registered successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@auth_router.post("/auth/login")
async def login_user(login_request: LoginRequest):
    user = await authenticate_user(login_request.email, login_request.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
   
    # #Generate JWT token
    token = create_access_token({"sub": user.email})
    return {"email": user.email, "access_token": token, "token_type": "bearer"}