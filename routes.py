from fastapi import APIRouter, Body , Depends
from fastapi.encoders import jsonable_encoder
from user import fastapi_users, User
from database import (
    # add_profile,
    delete_profile,
    retrieve_profile,
    retrieve_profiles,
    update_profile,
)
from models import (
    PostSchema,
    UpdatePostModel,
    ProfileSchema,
    UpdateProfileModel,
     ErrorResponseModel,
     ResponseModel,
)

router = APIRouter()
from fastapi import   HTTPException


@router.get("/", response_description="Profiles retrieved")
async def get_profiles():
    profiles = await retrieve_profiles()
    if profiles:
        return ResponseModel(profiles, "Profiles data retrieved successfully")
    return ResponseModel(profiles, "Empty list returned")

from pydantic import UUID4

@router.get("/{user_uuid}", response_description="Profile data retrieved UUDI=393e1871-05de-4b94-8679-701a27ba4b55")
async def get_profile_data(user_uuid:str):
    profile = await retrieve_profile(user_uuid)
    if profile=={"error":"error"}:
        raise HTTPException(status_code=404, detail="Profile doesn't exist.")
    if profile:
        return ResponseModel(profile, "Profile data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Profile doesn't exist.")


@router.put("/{user_uuid}")
async def update_profile_data(user_uuid:str,req:UpdateProfileModel=Body(...),user: User = Depends(fastapi_users.get_current_user)):
    reqq={k:v for k,v in req.dict().items() if v is not None} 
    updated_profile=await update_profile(user_uuid,reqq)
    if updated_profile==None :
        return ErrorResponseModel(
            "An error occurred",
            404,
            "error updating data",
        )
    else :
        return ResponseModel(
            "Profile with ID: {} name update is successful".format(user_uuid),
            "Profile name updated successfully",
        )
 
#hay que buscar como borrar el perfil si el user se elimina

@router.delete("/{user_uuid}",response_description="Profile data deleted from the database")
async def delete_profile_data(user_uuid:str,user: User = Depends(fastapi_users.get_current_user)):
    deleted_profile=await delete_profile(user_uuid)
    if deleted_profile:
        return ResponseModel(
            "Profile with ID: {} removed".format(id), "Profile deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Profile with id {0} doesn't exist".format(id)
    )