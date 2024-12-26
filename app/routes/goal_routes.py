from fastapi import FastAPI, HTTPException, Depends, APIRouter
from models import LearningGoal
from services.learning_goal_service import save_user_goals, fetch_user_goals
from utils.token_utils import decode_access_token 
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv

load_dotenv()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
goals_router=APIRouter()

@goals_router.post("/user/goals")
async def set_user_goals(
    learning_goal: LearningGoal,
    token: str = Depends(oauth2_scheme),
):
    """
    Save learning goals for a user after validating the JWT token.
    """
    try:
        # Decode and validate the JWT token
        payload = decode_access_token(token)
        user_email = payload.get("sub")

        if user_email != learning_goal.user_email:
            raise HTTPException(status_code=403, detail="Token does not match user email")

        # Save learning goals for the authenticated user
        await save_user_goals(learning_goal.user_email, learning_goal.goals, learning_goal.interests)
        return {"message": "Learning goals saved successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    
@goals_router.get("/user/goals/{user_email}")
async def get_user_goals(user_email: str, token: str = Depends(oauth2_scheme)):
    """
    Retrieve learning goals for a user after validating the JWT token.
    """
    try:
        # Decode and validate the JWT token
        payload = decode_access_token(token)
        token_email = payload.get("sub")

        if token_email != user_email:
            raise HTTPException(status_code=403, detail="Token does not match user email")

        # Fetch learning goals for the authenticated user
        goals = await fetch_user_goals(user_email)
        return {"goals": goals}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))