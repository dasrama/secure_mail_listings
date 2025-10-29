import jwt
from fastapi import HTTPException
from backend.config.settings import Settings
from jwt.exceptions import PyJWTError



def verify_jwt(token: str) -> str:
    try:
        payload = jwt.decode(token, Settings().SECRET_KEY, algorithms=["HS256"])
        email = payload.get("email")
        if not email:
            raise HTTPException(status_code=401, detail="Email not found in token")
        return email
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
