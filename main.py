from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.openapi.utils import get_openapi
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from models.mailModel import SchemaSend
from utils.mailCore import Email
from utils.dates import getDtNow
import uuid
from config import settings
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

title = "Courrier"
description = "Custom email api"
version = "1.0.0"

app = FastAPI(title=title, docs_url=None, redoc_url=None)

security = HTTPBasic()

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, settings.userEmail)
    correct_password = secrets.compare_digest(credentials.password, settings.userPassword)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/healthcheck")
def health_check():
    return {"date": str(getDtNow()),
            "id": uuid.uuid4()}

def sendMail(name=None, sender=None, subject=None, emailType=None, sendTo=None, emailContent=None):
        email=Email()
        email.setServer(server=settings.server,port=settings.port)
        email.setServerFromAddr(sender)
        email.setServerFromName(name)
        email.setSubject(subject)
        email.setEmailType(emailType)
        email.setContent(emailContent)
        email.addToAddr(sendTo)
        email.setDkimPrivateKeyPath(settings.dkimKey)
        email.send()
        return {'ok': 'send'}
        

@app.post("/mail", dependencies=[Depends(get_current_username)])
def send_mail(item: SchemaSend):
    try:
        if item.replyTo == settings.replyTo:
            res = sendMail(name=item.name, sender=item.sender, sendTo=item.sendTo, subject=item.subject, emailType=item.emailType, emailContent=item.emailContent)
        else:
            res = {"body": "can't get replyTo"}
        return res
    except Exception as res:    
        return res

@app.get("/docs", include_in_schema=False)
def overridden_swagger():
	return get_swagger_ui_html(
     openapi_url="/openapi.json", 
     title=app.title + " - Swagger UI",
     swagger_favicon_url=""
     )

@app.get("/redoc", include_in_schema=False)
def overridden_redoc():
	return get_redoc_html(
     openapi_url="/openapi.json", 
     redoc_favicon_url="",
     title=app.title + " - ReDoc"
     )


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=title,
        version=version,
        description=description,
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": ""
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi