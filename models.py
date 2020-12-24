from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field
from bson import ObjectId


# extend profile:
class PyObjectId(ObjectId):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectid')
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')


class ProfileSchema(BaseModel):
    pic: str = Field(...)
    user: Optional[PyObjectId] = Field(alias='user')

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }
        schema_extra = {
            "example": {
                "user": "5fd5158379f15ab4c0693f7f",
                "pic": "/asd.jpg",
            }

        }


class UpdateProfileModel(BaseModel):
    pic: str = Field(...)
    # profile: Optional[PyObjectId] = Field(alias='profile')

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }
        schema_extra = {
            "example": {
                "pic": "/asd.jpg",
            }
        }


class PostSchema(BaseModel):
    pic: List[str] = []
    text: str = Field(...)
    likes: List[PyObjectId] = []
    comments: List[PyObjectId] = []
    comment_id: Optional[PyObjectId] = Field(alias='main_coment')
    user: PyObjectId = Field(alias='user')

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }
        schema_extra = {

            "example": {

                "pic": ["/asd.jpg"],

                "text": "beautiful post",
                "likes": [
                    "5fd5158379f15ab4c0693f7f",
                    "5fd5158379f15ab4c0693f7g"
                ],
                "comments": [
                    "5fd5158379f15ab4c0693f7f",
                    "5fd5158379f15ab4c0693f7g"
                ],
                "comment_id":  "5fd5158379f15ab4c0693f7e",
                "user":  "5fd5158379f15ab4c0693f7f"

            }

        }


class UpdatePostModel(BaseModel):
    pic: List[str] = []
    text: str = Field(...)
    likes: List[PyObjectId] = []
    comments: List[PyObjectId] = []
    # comment_id: Optional[PyObjectId] = Field(alias='main_coment')
    # user: PyObjectId = Field(alias='user')

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }
        schema_extra = {

            "example": {

                "pic": ["/asd.jpg"],
                "text": "beautiful post",
                "likes": 1,
                "comments": [
                    "5fd5158379f15ab4c0693f7f",
                    "5fd5158379f15ab4c0693f7g",
                ]

            }

        }


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}
