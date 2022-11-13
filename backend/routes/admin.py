import json
from fastapi import APIRouter, status, HTTPException, Depends
from models.admin import AdminModel, AdminLogin
from database import admins_collection
from utils import serializeDict, serializeList
from auth.auth_handler import signJWT, decodeJWT
from passlib.hash import pbkdf2_sha256
from auth.auth_bearer import JWTBearer
from bson.objectid import ObjectId
router = APIRouter()


@router.get("/api/admins/", tags=["Admins"])
async def get_admins() -> dict:
    admins = serializeList(admins_collection.find())
    return {"admins": admins}

# Sign up


@router.post('/api/auth/signup/admin', tags=["Admins"], status_code=status.HTTP_201_CREATED)
async def sign_up(input_data: AdminModel):
    admin = AdminModel(
        nom=input_data.nom,
        prenom=input_data.prenom,
        adminname=input_data.adminname,
        email=input_data.email,
        password=pbkdf2_sha256.hash(
            input_data.password)  # Hashing before storing
    )

    db_admin = admins_collection.insert_one(dict(admin))
    admin_id = str(db_admin.inserted_id)
    return signJWT(admin_id)

# Login


def check_admin(data: AdminLogin):
    for admin in list(admins_collection.find()):
        if admin["adminname"] == data.adminname and pbkdf2_sha256.verify(data.password, admin["password"]):
            return str(admin["_id"])
    return False


@router.post('/api/auth/login/admin', tags=["Admins"])
async def login(input_data: AdminLogin):
    admin_id_returned = check_admin(input_data)
    if check_admin(input_data) != False:
        return signJWT(admin_id_returned)  # 200 # Returns JWT Access token

    raise HTTPException(
        status_code=401, detail="Nom d'utilisateur ou mot de passe incorrect")


@router.get("/api/admins/me", dependencies=[Depends(JWTBearer())], tags=["Get admin Data"])
async def get_admin_data(token: str = Depends(JWTBearer())) -> dict:
    # {"admin_id": "....", "expires": ... }
    decoded_payload = serializeDict(decodeJWT(token))
    admin_id = decoded_payload['admin_id']
    all_matched_admins = serializeList(
        admins_collection.find({'_id': ObjectId(str(admin_id))}))
    return all_matched_admins[0]
