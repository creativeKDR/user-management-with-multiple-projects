from fastapi import APIRouter, status, Depends, HTTPException

from config import Config as config
from repository import UserRepository
from schemas import CreateUserResponse, RequestModel, UpdateUserResponse

router = APIRouter(prefix=f'/api/{config.version}')


# API endpoints
@router.get('/get_users', status_code=status.HTTP_200_OK, response_model=list[dict])
async def get_users(repository: UserRepository = Depends(UserRepository)) -> list[dict]:
    # fetch all user details
    response = await repository.get()
    return response


@router.post('/add_users', status_code=status.HTTP_201_CREATED, response_model=CreateUserResponse)
async def add_users(request: RequestModel, repository: UserRepository = Depends(UserRepository)) -> any:
    # add new user details
    response = await repository.create(request=request)
    if not response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not created")
    return CreateUserResponse(message="User created Successfully", user_id=response[1], user_details=response[0])


@router.put('/update_users', status_code=status.HTTP_200_OK, response_model=UpdateUserResponse)
async def update_users(request: RequestModel, user_id: str,
                       repository: UserRepository = Depends(UserRepository)) -> any:
    # update the user details
    response = await repository.update(request=request, user_id=user_id)
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
