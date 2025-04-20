import requests
from datetime import datetime
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from datetime import timedelta
import jwt

from backend.models.auth import GoogleToken
from backend.config.settings import Settings
from fastapi.responses import RedirectResponse


FRONTEND_URL = "http://localhost:8501" 

router = APIRouter()

def create_access_token(email: str):
    expire = datetime.now() + timedelta(hours=1)
    payload = {"email": email, "exp": expire}
    token = jwt.encode(payload, Settings().SECRET_KEY, algorithm="HS256")
    return token

@router.get("/login")
def login_with_google():
    auth_url = (
        f"https://accounts.google.com/o/oauth2/v2/auth"
        f"?client_id={Settings().GOOGLE_CLIENT_ID}"
        f"&redirect_uri={Settings().GOOGLE_REDIRECT_URI}"
        f"&response_type=code"
        f"&scope={Settings().GOOGLE_SCOPE}"
        f"&access_type=offline"
        f"&prompt=consent"
    )
    return RedirectResponse(auth_url)

@router.get("/callback")
async def google_auth_callback(request: Request):
    code = request.query_params.get("code")

    token_resp = requests.post("https://oauth2.googleapis.com/token", data={
        "code": code,
        "client_id": Settings().GOOGLE_CLIENT_ID,
        "client_secret": Settings().GOOGLE_CLIENT_SECRET,
        "redirect_uri": Settings().GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code"
    })

    tokens = token_resp.json()
    # print(tokens)
    access_token = tokens.get("access_token")
    id_token_str = tokens.get("id_token")

    if not id_token_str:
        raise HTTPException(status_code=400, detail="No ID token returned from Google.")

    try:
        idinfo = id_token.verify_oauth2_token(id_token_str, google_requests.Request(), Settings().GOOGLE_CLIENT_ID)
        user_email = idinfo.get("email")

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"ID token verification failed: {e}")

    if not user_email:
        raise HTTPException(status_code=400, detail="Failed to extract email from ID token.")

    existing_token = await GoogleToken.find_one(GoogleToken.email == user_email)

    if existing_token:
        existing_token.access_token = access_token
        existing_token.refresh_token = tokens.get("refresh_token")
        existing_token.expires_in = tokens.get("expires_in")
        existing_token.token_type = tokens.get("token_type")
        existing_token.scope = tokens.get("scope")
        existing_token.created_at = datetime.now()
        await existing_token.save()
    else:
        token_doc = GoogleToken(
            email=user_email,
            access_token=access_token,
            refresh_token=tokens.get("refresh_token"),
            expires_in=tokens.get("expires_in"),
            token_type=tokens.get("token_type"),
            scope=tokens.get("scope"),
            created_at=datetime.now()
        )
        await token_doc.insert()

    jwt_token = create_access_token(user_email)

    print(jwt_token)
    print(user_email)
    return RedirectResponse(url=f"{FRONTEND_URL}/?token={jwt_token}&email={user_email}")
