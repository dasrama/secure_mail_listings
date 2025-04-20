from fastapi import APIRouter, HTTPException, Request
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from backend.models.auth import GoogleToken
from backend.config.settings import Settings
import requests

router = APIRouter()

from backend.auth.verify_jwt import verify_jwt

@router.get("/")
async def fetch_emails(request: Request):
    token = request.headers.get("Authorization")
    print(request)
    print("token(backend): ", token)
    
    if not token:
        print("token not found")
        raise HTTPException(status_code=401, detail="Missing Authorization token")

    token = token.split(" ")[1]

    try:
        user_email = verify_jwt(token)
        print(user_email)

        token_doc = await GoogleToken.find_one(GoogleToken.email == user_email)
        
        if not token_doc:
            raise HTTPException(status_code=404, detail="Google token not found for the user.")
        
        service = get_gmail_service(token_doc)
        emails = get_emails(service)
        return emails

    except Exception as e:
        print("error: ",e)
        raise HTTPException(status_code=401, detail="Invalid token or authentication failed.")

def get_gmail_service(token_doc: GoogleToken):
    creds = Credentials(
        token=token_doc.access_token,
        refresh_token=token_doc.refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=Settings().GOOGLE_CLIENT_ID,
        client_secret=Settings().GOOGLE_CLIENT_SECRET,
        scopes=["https://www.googleapis.com/auth/gmail.readonly"]
    )
    service = build("gmail", "v1", credentials=creds)
    print(service)
    return service

def get_emails(service, max_results=10):
    results = service.users().messages().list(userId="me", maxResults=max_results).execute()
    messages = results.get("messages", [])

    email_list = []

    for msg in messages:
        msg_data = service.users().messages().get(userId="me", id=msg["id"]).execute()

        headers = msg_data.get("payload", {}).get("headers", [])
        parts = msg_data.get("payload", {}).get("parts", [])

        subject = next((h["value"] for h in headers if h["name"] == "Subject"), "No Subject")
        sender = next((h["value"] for h in headers if h["name"] == "From"), "Unknown Sender")

        attachments = []
        for part in parts:
            if part.get("filename"):
                attachments.append(part.get("filename"))

        email_list.append({
            "subject": subject,
            "email_address": sender,
            "documents": attachments,
            "timestamp": msg_data.get("internalDate")
        })

    return email_list
