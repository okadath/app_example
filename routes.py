from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

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


# @router.post("/", response_description="Profile data added into the database")
# async def add_student_data(profile: ProfileSchema = Body(...)):
#     profile = jsonable_encoder(profile)
#     new_profile = await add_profile(profile)
#     if new_profile==[]:
#         raise HTTPException(status_code=404, detail="Profile name already exists")
#     return ResponseModel(new_profile, "Profile added successfully.")


@router.get("/", response_description="Profiles retrieved")
async def get_profiles():
    profiles = await retrieve_profiles()
    if profiles:
        return ResponseModel(profiles, "Profiles data retrieved successfully")
    return ResponseModel(profiles, "Empty list returned")
