import jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status, Depends
from jwt.exceptions import PyJWTError
from datetime import datetime, timedelta

from backend.models.auth import Token, TokenData
from backend.config.settings import Settings
from backend.models.user import User


settings = Settings()

oauth_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def create_access_token(data: dict) -> Token:
    to_encode = data.copy()
    expiry = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expiry})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credential_exception) -> TokenData:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        id: str = payload.get("user_id")

        if not id:
            raise credential_exception

        token_data = TokenData(id=id) 
        return token_data
    except PyJWTError:
        raise credential_exception

async def get_current_user(token: str = Depends(oauth_scheme)):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    token_data = verify_access_token(token, credential_exception)
    user = await User.get(token_data.id)
    if not user:
        raise credential_exception
    return user
