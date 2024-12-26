from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from pydantic import BaseModel, EmailStr
from typing import List

# ================== SQLAlchemy Models ==================

# User Model
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)

    # One-to-Many relationship with Learning Goals
    learning_goals = relationship("LearningGoalDB", back_populates="user")


# LearningGoal Model
class LearningGoalDB(Base):
    __tablename__ = "learning_goals"
    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String, ForeignKey("users.email"), nullable=False)  # Many-to-One relationship
    goal = Column(String(255), nullable=False)
    interest = Column(String(255), nullable=False)

    # Many-to-One relationship with User
    user = relationship("User", back_populates="learning_goals")


# ================== Pydantic Schemas ==================

# User Pydantic Schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr
    is_active: bool = True

class UserCreate(UserBase):
    password: str

class UserInDB(UserBase):
    hashed_password: str


# Login Request Schema
class LoginRequest(BaseModel):
    email: str
    password: str

class PromptRequest(BaseModel):
    prompt: str

# LearningGoal Pydantic Schemas
class LearningGoal(BaseModel):
    user_email: str
    goals: List[str]
    interests: List[str]

    class Config:
        from_attributes = True


