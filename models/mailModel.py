from pydantic import BaseModel, EmailStr

class SchemaSend(BaseModel):
    sender: EmailStr
    name: str
    subject: str
    emailType: str
    emailContent: str
    sendTo: EmailStr
    replyTo: EmailStr