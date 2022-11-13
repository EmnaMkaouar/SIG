import json
from fastapi import APIRouter, status, HTTPException, Depends
from models.users import UserModel, UserLogin
from database import users_collection
from utils import serializeDict, serializeList
from auth.auth_handler import signJWT, decodeJWT
from passlib.hash import pbkdf2_sha256
from auth.auth_bearer import JWTBearer
from bson.objectid import ObjectId
router = APIRouter()


@router.get("/api/users/", tags=["Users"])
async def get_users() -> dict:
    users = serializeList(users_collection.find())
    return {"users": users}

# Sign up


@router.post('/api/auth/signup/', tags=["Users"], status_code=status.HTTP_201_CREATED)
async def sign_up(input_data: UserModel):
    user = UserModel(
        nom=input_data.nom,
        prenom=input_data.prenom,
        username=input_data.username,
        email=input_data.email,
        password=pbkdf2_sha256.hash(
            input_data.password)  # Hashing before storing
    )

    db_user = users_collection.insert_one(dict(user))
    user_id = str(db_user.inserted_id)
    return signJWT(user_id)

# Login


def check_user(data: UserLogin):
    for user in list(users_collection.find()):
        if user["username"] == data.username and pbkdf2_sha256.verify(data.password, user["password"]):
            return str(user["_id"])
    return False


@router.post('/api/auth/login/', tags=["Users"])
async def login(input_data: UserLogin):
    user_id_returned = check_user(input_data)
    if check_user(input_data) != False:
        return signJWT(user_id_returned)  # 200 # Returns JWT Access token

    raise HTTPException(
        status_code=401, detail="Nom d'utilisateur ou mot de passe incorrect")


@router.get("/api/users/me", dependencies=[Depends(JWTBearer())], tags=["Get User Data"])
async def get_user_data(token: str = Depends(JWTBearer())) -> dict:
    # {"user_id": "....", "expires": ... }
    decoded_payload = serializeDict(decodeJWT(token))
    user_id = decoded_payload['user_id']
    all_matched_users = serializeList(
        users_collection.find({'_id': ObjectId(str(user_id))}))
    return all_matched_users[0]
