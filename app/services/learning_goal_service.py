from repositories.learning_goal_repository import insert_learning_goals, find_learning_goals_by_email

async def save_user_goals(user_email: str, goals: list, interests: list):
    """
    Save learning goals for a user.
    """
    await insert_learning_goals(user_email, goals, interests)

async def fetch_user_goals(user_email: str):
    """
    Retrieve learning goals for a user.
    """
    return await find_learning_goals_by_email(user_email)
