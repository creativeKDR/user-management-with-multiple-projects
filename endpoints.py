from typing import Union

from fastapi import APIRouter, status, Depends, HTTPException

from config import Config as config
from repository import UserRepository
from schemas import ProjectOneUser, ProjectTwoUser, ProjectThreeUser, CreateUserResponse

router = APIRouter(prefix=f'/api/{config.version}')


@router.get('/{source}/get_users', status_code=status.HTTP_200_OK, response_model=list[dict])
async def get_users(repository: UserRepository = Depends(UserRepository)) -> list[dict]:
    response = await repository.get()
    return response


@router.post('/{source}/add_users', status_code=status.HTTP_201_CREATED, response_model=CreateUserResponse)
async def add_users(source: str, request: Union[ProjectOneUser, ProjectTwoUser, ProjectThreeUser],
                    repository: UserRepository = Depends(UserRepository)) -> any:
    response = await repository.create(source=source, request=request)
    if not response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not created")
    return CreateUserResponse(message="User created Successfully", user_id=response[1], user_details=response[0])


@router.put('/{source}/update_users', status_code=status.HTTP_200_OK, response_model=Union[ProjectOneUser, ProjectTwoUser, ProjectThreeUser])
async def update_users(source: str, request: Union[ProjectOneUser, ProjectTwoUser, ProjectThreeUser], user_id: str,
                       repository: UserRepository = Depends(UserRepository)) -> any:
    response = await repository.update(source=source, request=request, user_id=user_id)
    if not response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return response


@router.delete('/delete_user', status_code=status.HTTP_200_OK, response_model=dict)
async def delete_users(user_id: str, repository: UserRepository = Depends(UserRepository)) -> dict:
    response = await repository.delete(user_id=user_id)
    if not response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return response
