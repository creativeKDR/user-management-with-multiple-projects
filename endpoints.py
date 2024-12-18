from fastapi import APIRouter, status, Depends, HTTPException

from config import Config as config
from utils import Utilities as utils
from repository import UserRepository
from schemas import CreateUserResponse, RequestModel, UpdateUserResponse

router = APIRouter(prefix=f'/api/{config.version}')


# API endpoints
@router.get('/{project_source}/get_users', status_code=status.HTTP_200_OK, response_model=list[dict])
async def get_users(project_source: str, repository: UserRepository = Depends(UserRepository)) -> list[dict]:
    # fetch all user details
    model = utils.check_model_source(project_source)
    if model:
        return await repository.get(project_id=project_source)


@router.post('/{project_source}/add_users', status_code=status.HTTP_201_CREATED, response_model=CreateUserResponse)
async def add_users(project_source: str, request: RequestModel,
                    repository: UserRepository = Depends(UserRepository)) -> any:
    # add new user details
    model = utils.check_model_source(project_source)
    if model:
        response = await repository.create(request=request, project_source=project_source, model=model)
        if not response:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not created")
        return CreateUserResponse(message="User created Successfully", user_id=response[1], user_details=response[0])


@router.put('/{project_source}/update_users', status_code=status.HTTP_200_OK, response_model=UpdateUserResponse)
async def update_users(request: RequestModel, user_id: str, project_source: str,
                       repository: UserRepository = Depends(UserRepository)) -> any:
    # update the user details
    model = utils.check_model_source(project_source)
    if model:
        response = await repository.update(request=request, user_id=user_id, model=model, project_source=project_source)
        if not response:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return UpdateUserResponse(message='User updated successfully', user_details=response)


@router.delete('/delete_user', status_code=status.HTTP_200_OK, response_model=dict)
async def delete_users(user_id: str, repository: UserRepository = Depends(UserRepository)) -> dict:
    # delete the user details
    response = await repository.delete(user_id=user_id)
    if not response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return response
