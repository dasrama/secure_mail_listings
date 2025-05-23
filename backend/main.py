from fastapi import FastAPI
from contextlib import asynccontextmanager

from backend.config.config import initiate_database
from backend.routers.email import router as EmailRouter
from backend.routers.auth import router as AuthRouter


@asynccontextmanager
async def lifespan(app: FastAPI):
    await initiate_database()
    yield
    print("Shutting down server")

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Hello, World!"}

app.include_router(router=EmailRouter, tags=["Email"], prefix="/emails")
app.include_router(router=AuthRouter, tags=["Auth"], prefix="/auth")
