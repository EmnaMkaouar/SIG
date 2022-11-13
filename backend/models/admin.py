from pydantic import BaseModel, Field, EmailStr, validator
from database import admins_collection
from utils import serializeDict, serializeList
from datetime import datetime
# EmailStr <=> Email Structure
# BaseModel Helps in serialization et de-serialization
# Field(...)  <=>  required Field

class AdminModel(BaseModel):
    nom             : str       = Field()
    prenom          : str       = Field()
    adminname        : str       = Field(...)
    email           : EmailStr  = Field(...)
    password        : str       = Field(...)
    last_joined     : datetime  = None
    creation_date   : datetime  = None

    @validator('adminname')
    def adminname_must_be_unique(cls, v):
        all_admins = serializeList(admins_collection.find())
        all_adminnames = []
        for admin in all_admins:
            all_adminnames.append(admin['adminname'].upper())
        if v.upper() in all_adminnames:
            raise ValueError("Le nom d'utilisateur est déjà utilisé")
        return v.title()

        
    @validator('email')
    def email_must_be_unique(cls, v):
        all_admins = serializeList(admins_collection.find())
        all_emails = []
        for admin in all_admins:
            all_emails.append(admin['email'].upper())
        if v.upper() in all_emails:
            raise ValueError("L'e-mail est déjà utilisé")
        return v.title()


class AdminLogin(BaseModel):
    adminname    : str   = Field(...)
    password    : str   = Field(...)
