from fastapi import APIRouter

from backend.models.email import Email, CreateEmail


router = APIRouter()

@router.post("/")
async def email_reader(email: CreateEmail):
    email_document = Email(
            email_address=email.email_address,
            subject=email.subject,
            documents=email.documents
        )
    
    await email_document.insert()
        
    return {"message": "Email inserted successfully!"}
    
