from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from database import async_session
from models import User  # Ensure this matches your User model definition

async def insert_user(user_dict: dict):
    async with async_session() as session:
        async with session.begin():
            user = User(**user_dict)  # Convert the dictionary to a User object
            session.add(user)         # Add the new user to the session
        await session.commit()        # Commit the transaction
    return user

async def find_user_by_email(email: str):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.email == email))
        user = result.scalars().first()  # Retrieve the first matching user
        return user
