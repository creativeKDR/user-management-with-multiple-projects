from datetime import date
from typing import Union, Annotated, Literal
from uuid import UUID

from fastapi import Body
from pydantic import BaseModel, Field, EmailStr


# Request Models

class User(BaseModel):
    first_name: str = Field(min_length=3, alias='first_name')
    last_name: str = Field(min_length=3, alias='last_name')
    project_id: Union[str, UUID] = Field(alias='project_id')

    class Config:
        arbitrary_types_allowed = True


class ProjectOneUser(User):
    model_type: Literal['p1'] = None
    company_name: str = Field(min_length=3, alias='company_name')
    email: EmailStr = Field(alias='email')
    password: str = Field(min_length=6, alias='password')


class ProjectTwoUser(User):
    model_type: Literal['p2'] = None
    mobile_no: str = Field(max_length=10, alias='mobile_no')
    hashtag: str = Field(min_length=3, alias='hashtag')


class ProjectThreeUser(User):
    model_type: Literal['p3'] = None
    mobile_no: str = Field(max_length=10, alias='mobile_no')
    dob: date = Field(alias='dob')


# Create a new model to represent the discriminated union
RequestModel = Annotated[Union[ProjectOneUser, ProjectTwoUser, ProjectThreeUser], Body(..., discriminator='model_type')]


# Response Models
class CreateUserResponse(BaseModel):
    message: str
    user_id: str
    user_details: Union[ProjectOneUser, ProjectTwoUser, ProjectThreeUser]


class UpdateUserResponse(BaseModel):
    message: str
    user_details: Union[ProjectOneUser, ProjectTwoUser, ProjectThreeUser]
