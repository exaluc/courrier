from fastapi import APIRouter, Depends
from models.mailModel import SchemaSend
from utils.mailCore import Email
from config import settings
from security.depends import getCurrentUsername

router = APIRouter()

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
        

@router.post("/", dependencies=[Depends(getCurrentUsername)])
def send_mail(item: SchemaSend):
    try:
        if item.replyTo == settings.replyTo:
            res = sendMail(name=item.name, sender=item.sender, sendTo=item.sendTo, subject=item.subject, emailType=item.emailType, emailContent=item.emailContent)
        else:
            res = {"body": "can't get replyTo"}
        return res
    except Exception as res:    
        return res