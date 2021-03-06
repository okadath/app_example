import motor.motor_asyncio
from fastapi import FastAPI, Request, Depends, Response
from fastapi_users import FastAPIUsers, models
from fastapi_users.authentication import JWTAuthentication
from fastapi_users.db import MongoDBUserDatabase 


DATABASE_URL = "mongodb://localhost:27017"
# openssl rand -hex 32
SECRET = "8d6779097e486aec0e62f353165cbd548d3a153b466f3d8141dd9dbf99fddef2"


class User(models.BaseUser):
    pass


class UserCreate(models.BaseUserCreate):
    pass


class UserUpdate(User, models.BaseUserUpdate):
    pass


class UserDB(User, models.BaseUserDB):
    pass


client = motor.motor_asyncio.AsyncIOMotorClient(
    DATABASE_URL, uuidRepresentation="standard"
)
db = client["data_app"]
collection_users = db["users"]
collection_profiles = db["profiles"]
user_db = MongoDBUserDatabase(UserDB, collection_users)

collection_profiles.create_index("user", unique=True)

from bson.objectid import ObjectId



async def on_after_register(user: UserDB, request: Request):
    try:
        # uuser=await collection_users.insert_one(user)#ya trae inserted_id?
        profile=await collection_profiles.insert_one({
            "user":user.id,
            "pic":"",
            })
    except  Exception as e:
        # print(e)
        raise e
        return []
    # print(f"User {user.id} has registered.")


def on_after_forgot_password(user: UserDB, token: str, request: Request):
    pass
    # print(f"User {user.id} has forgot their password. Reset token: {token}")


jwt_authentication = JWTAuthentication(
    secret=SECRET, lifetime_seconds=3600, tokenUrl="/auth/jwt/login"
)

app = FastAPI()
fastapi_users = FastAPIUsers(
    user_db,
    [jwt_authentication],
    User,
    UserCreate,
    UserUpdate,
    UserDB,
)
app.include_router(
    fastapi_users.get_auth_router(jwt_authentication), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(on_after_register), prefix="/auth", tags=["auth"]
)
# app.include_router(
#     fastapi_users. #get_register_router(on_after_register), prefix="/auth", tags=["auth"]
# )
app.include_router(
    fastapi_users.get_reset_password_router(
        SECRET, after_forgot_password=on_after_forgot_password
    ),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(fastapi_users.get_users_router(), prefix="/users", tags=["users"])


@app.post("/auth/jwt/refresh", tags=["auth"]) 
async def refresh_jwt( response: Response, user=Depends(fastapi_users.get_current_active_user)):
    print(user)
    print(response)
    return await jwt_authentication.get_login_response(user, response)

