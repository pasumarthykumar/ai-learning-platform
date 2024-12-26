from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import LearningGoalDB
from database import async_session

async def insert_learning_goals(user_email: str, goals: list, interests: list):
    """
    Inserts learning goals and interests for a user.
    """
    async with async_session() as session:
        async with session.begin():
            for goal, interest in zip(goals, interests):
                learning_goal = LearningGoalDB(user_email=user_email, goal=goal, interest=interest)
                session.add(learning_goal)  # Add the learning goal to the session
        await session.commit()  # Commit the transaction

async def find_learning_goals_by_email(user_email: str):
    """
    Retrieves all learning goals for a specific user by their email.
    """
    async with async_session() as session:
        result = await session.execute(select(LearningGoalDB).where(LearningGoalDB.user_email == user_email))
        learning_goals = result.scalars().all()  # Retrieve all matching goals
        return learning_goals
