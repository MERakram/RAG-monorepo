from fastapi import APIRouter, Depends, HTTPException
from grpc import Status
from starlette.status import HTTP_200_OK
from typing import Annotated
from app.core.dependencies import (
    get_users_dep,
    delete_user_dep,
    onboard_user_action_dep,
    update_user_dep,
    get_user_id_dep,
    require_active_user,
    require_admin,
    get_mongodb_repo,
)
from app.repository.user import UserRepository
from loguru import logger
from app.schema.user import ListUsersResponse, UpdateUserResponse, User


router = APIRouter()


# Get list of users with sorting options
@router.get(
    "/",
    status_code=HTTP_200_OK,
    response_description="get users list",
    name="user: list_users",
    response_model_exclude_none=True,
    response_model=ListUsersResponse,
)
def get_users_list(
    current_user: Annotated[User, Depends(require_admin)],
    usersList: ListUsersResponse = Depends(get_users_dep),
):
    logger.info(f"Admin user '{current_user.username}' requested to list users.")
    return usersList


# Get user by ID
@router.get(
    "/{userId}",
    status_code=HTTP_200_OK,
    response_description=" get user by id",
    name="user: get_by_id",
    response_model_exclude_none=True,
    response_model=User,
)
def get_user_by_id(
    current_user: Annotated[User, Depends(require_admin)],
    retrieved_user: User = Depends(get_user_id_dep),
):
    return retrieved_user


# Delete user by ID
@router.delete(
    "/{userId}",
    status_code=HTTP_200_OK,
    response_description="delete user by id",
    name="user: delete_by_id",
    response_model_exclude_none=True,
)
def delete_user_by_id(
    current_user: Annotated[User, Depends(require_admin)],
    userId=Depends(delete_user_dep),
):
    return userId


# Update user by ID
@router.patch(
    "/{userId}",
    status_code=HTTP_200_OK,
    response_description="update user",
    name="user: update",
    response_model_exclude_none=True,
     response_model=User, 
)
def update_user(
    request_body: UpdateUserResponse,
    current_user: Annotated[User, Depends(require_active_user)],
    userId=Depends(update_user_dep),
    user_repo: UserRepository = Depends(get_mongodb_repo(UserRepository)),
) -> UpdateUserResponse:
    if current_user.user_id != userId and current_user.role != "admin":
        raise HTTPException(
            status_code=Status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this user"
        )
    
    # If admin is updating another user, or user is updating themselves
    updated_user = update_user_dep(ID=userId, req=request_body, user_repo=user_repo)
    return updated_user

# Onboard / Activate a user (Admin only)
@router.post(
    '/{userId}/onboard',
    status_code=HTTP_200_OK,
    response_description='User onboarded and activated successfully',
    name='user:onboard',
    response_model=User,
)
def onboard_user(
    admin_user: User = Depends(require_admin), 
    activated_user: User = Depends(onboard_user_action_dep) 
):
    """
    Onboards a user, setting them as active. Requires admin privileges.
    """
    return activated_user