from pydantic import BaseModel, Field, EmailStr, validator
from database import users_collection
from utils import serializeDict, serializeList
from datetime import datetime
# EmailStr <=> Email Structure
# BaseModel Helps in serialization et de-serialization
# Field(...)  <=>  required Field

class UserModel(BaseModel):
    nom             : str       = Field()
    prenom          : str       = Field()
    username        : str       = Field(...)
    email           : EmailStr  = Field(...)
    password        : str       = Field(...)
    last_joined     : datetime  = None
    creation_date   : datetime  = None

    @validator('username')
    def username_must_be_unique(cls, v):
        all_users = serializeList(users_collection.find())
        all_usernames = []
        for user in all_users:
            all_usernames.append(user['username'].upper())
        if v.upper() in all_usernames:
            raise ValueError("Le nom d'utilisateur est déjà utilisé")
        return v.title()

        
    @validator('email')
    def email_must_be_unique(cls, v):
        all_users = serializeList(users_collection.find())
        all_emails = []
        for user in all_users:
            all_emails.append(user['email'].upper())
        if v.upper() in all_emails:
            raise ValueError("L'e-mail est déjà utilisé")
        return v.title()


class UserLogin(BaseModel):
    username    : str   = Field(...)
    password    : str   = Field(...)
