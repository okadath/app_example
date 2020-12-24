
from fastapi import FastAPI

# from .routes.student import router as StudentRouter
from routes import router as ProfileRouter

from user import    app
# app = FastAPI()

# app.include_router(StudentRouter, tags=["Student"], prefix="/student")

app.include_router(ProfileRouter, tags=["Profile"], prefix="/profile")