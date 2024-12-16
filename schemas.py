from datetime import date
from typing import Optional, Union
from uuid import UUID

from pydantic import BaseModel, Field, EmailStr


class User(BaseModel):
    first_name: str = Field(min_length=3)
    last_name: str = Field(min_length=3)
    project_id: Union[str, UUID] = Field()


class ProjectOneUser(User):
    company_name: str = Field(min_length=3, default=None)
    email: EmailStr = Field()
    password: str = Field(min_length=6)


class ProjectTwoUser(User):
    mobile_no: str = Field(max_length=10)
    hashtag: Optional[str] = Field(min_length=3, default=None)


class ProjectThreeUser(User):
    mobile_no: str = Field(max_length=10)
    dob: date = Field()


class CreateUserResponse(BaseModel):
    message: str
    user_id: str
    user_details: Union[ProjectOneUser, ProjectTwoUser, ProjectThreeUser]

