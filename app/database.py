from fastapi import FastAPI, HTTPException
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from sqlalchemy.ext.declarative import declarative_base

app = FastAPI()

DATABASE_URL = "mysql+asyncmy://root:MahiDhoni%4012@localhost:3306/ai_learning_platform"


# Create an async engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create a sessionmaker
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

@app.get("/check-db-connection")
async def check_db_connection():
    try:
        # Test the connection
        async with engine.connect() as connection:
            await connection.execute(text("SELECT 1"))  # Simple query to test the connection
        return {"status": "success", "message": "Database connection is working!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {e}")


Base = declarative_base()
