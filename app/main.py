from fastapi import FastAPI
from routes.auth_routes import auth_router
from routes.goal_routes import goals_router
from routes.content_routes import content_router

app = FastAPI()

# Include routers
app.include_router(auth_router)
app.include_router(goals_router)
app.include_router(content_router)


    





    




    


