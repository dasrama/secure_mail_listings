from fastapi import APIRouter, HTTPException, status
from passlib.context import CryptContext

from backend.models.user import UserLogin, CreateUser, User
from backend.models.user import User
from backend.auth.jwt_handler import create_access_token


router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/register")
async def register(user: CreateUser):
    existing = await User.find_one(User.email == user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = pwd_context.hash(user.password)
    user = User(email=user.email, hashed_password=hashed_pw)
    await user.insert()
    return {"msg": "User registered"}

@router.post("/login")
async def login(user_input: UserLogin):
    user = await User.find_one(User.email == user_input.email)
    if not user or not pwd_context.verify(user_input.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token({"user_id": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}
