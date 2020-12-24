import motor.motor_asyncio
from user import db

# las definiciones no requieren ningun await

# MONGO_DETAILS="mongodb://localhost:27017"

# client=motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

# database = client.data_app
database=db
# student_collection = database.get_collection("students_collection")
profile_collection = database.get_collection("profiles")
profile_collection.create_index("user", unique=True)
# student_collection.create_index("fullname", unique=True)
# database.command(db.collection_name.createIndex( {field_name : 1} , {unqiue : true} ))
# from pydantic import 
from bson.objectid import ObjectId


def profile_helper(profile) -> dict:
    print(profile)
    return {
        "id":str(profile["_id"]),
        "pic":profile["pic"],
        "user":str(profile["user"]),
    }

from bson.objectid import ObjectId


async def retrieve_profiles():
    profiles=[]
    async for profile in profile_collection.find():
        profiles.append(profile_helper(profile))
    return profiles
from pydantic import UUID4

async def retrieve_profile(user__uuid:str)->dict:

    # if ObjectId.is_valid(user):
    print(user__uuid)
    profile= await  profile_collection.find_one({"user":UUID4(user__uuid)})
    if profile:
        return profile_helper(profile)
    print("error")
    return {"error":"error"}

async def update_profile(user__uuid:str,data:dict):
    if len(data)<1:
        return False
    profile=await profile_collection.find_one({"user":UUID4(user__uuid)})
    if profile:
        update_profile=await profile_collection.update_one(
            {"user":UUID4(user__uuid)},{"$set":data}
        )
    if update_profile:
        return True
    return False

async def delete_profile(user__uuid:str):
    profile=await profile_collection.find_one({"user":UUID4(user__uuid)})
    if profile:
        await profile_collection.delete_one({"user":UUID4(user__uuid)})
        return True
    return False