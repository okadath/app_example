import motor.motor_asyncio


# las definiciones no requieren ningun await

MONGO_DETAILS="mongodb://localhost:27017"

client=motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.data_app

# student_collection = database.get_collection("students_collection")
profile_collection = database.get_collection("profiles_collection")
profile_collection.create_index("user", unique=True)
# student_collection.create_index("fullname", unique=True)
# database.command(db.collection_name.createIndex( {field_name : 1} , {unqiue : true} ))


def profile_helper(profile) -> dict:
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


async def retrieve_profile(id:str)->dict:
    if ObjectId.is_valid(id):
        profile= await  profile_collection.find_one({"_id":ObjectId(id)})
        if profile:
            return profile_helper(profile)
    return {"error":"error"}

async def update_profile(id:str,data:dict):
    if len(data)<1:
        return False
    profile=await profile_collection.find_one({"_id":ObjectId(id)})
    if profile:
        update_profile=await profile_collection.update_one(
            {"_id":ObjectId(id)},{"$set":data}
        )
    if update_profile:
        return True
    return False

async def delete_profile(id:str):
    profile=await profile_collection.find_one({"_id":ObjectId(id)})
    if profile:
        await profile_collection.delete_one({"_id":ObjectId(id)})
        return True
    return False