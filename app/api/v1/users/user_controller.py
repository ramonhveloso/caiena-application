from typing import Annotated

from fastapi import APIRouter, Depends, Security
from sqlalchemy.orm import Session

from app.api.v1.users.user_repository import UserRepository
from app.api.v1.users.user_schemas import (
    DeleteUserResponse,
    GetUserResponse,
    GetUsersMeResponse,
    GetUsersResponse,
    PutUserRequest,
    PutUserResponse,
    PutUsersMeRequest,
    PutUsersMeResponse,
)
from app.api.v1.users.user_service import UserService
from app.middleware.dependencies import AuthUser, get_db, jwt_middleware

router = APIRouter()
user_service = UserService(UserRepository())


@router.get("/me")
async def get_users_me(
    authuser: Annotated[AuthUser, Security(jwt_middleware)],
    db: Session = Depends(get_db),
) -> GetUsersMeResponse:
    response_service = await user_service.get_authenticated_user(
        db=db, authuser=authuser
    )
    return GetUsersMeResponse.model_validate(response_service)


@router.put("/me")
async def put_users_me(
    data: PutUsersMeRequest,
    authuser: Annotated[AuthUser, Security(jwt_middleware)],
    db: Session = Depends(get_db),
) -> PutUsersMeResponse:
    response_service = await user_service.update_user_profile(
        db=db, authuser=authuser, data=data
    )
    return PutUsersMeResponse.model_validate(response_service)


@router.get("/")
async def get_users(
    authuser: Annotated[AuthUser, Security(jwt_middleware)],
    db: Session = Depends(get_db),
) -> GetUsersResponse:
    response_service = await user_service.get_all_users(db)
    return GetUsersResponse.model_validate(response_service)


@router.get("/{user_id}")
async def get_user(
    authuser: Annotated[AuthUser, Security(jwt_middleware)],
    user_id: int,
    db: Session = Depends(get_db),
) -> GetUserResponse:
    response_service = await user_service.get_user_by_id(db=db, user_id=user_id)
    return GetUserResponse.model_validate(response_service)


@router.put("/{user_id}")
async def put_user(
    authuser: Annotated[AuthUser, Security(jwt_middleware)],
    data: PutUserRequest,
    user_id: int,
    db: Session = Depends(get_db),
) -> PutUserResponse:
    response_service = await user_service.update_user(db=db, user_id=user_id, data=data)
    return PutUserResponse.model_validate(response_service)


@router.delete("/{user_id}")
async def delete_user(
    authuser: Annotated[AuthUser, Security(jwt_middleware)],
    user_id: int,
    db: Session = Depends(get_db),
) -> DeleteUserResponse:
    response_service = await user_service.delete_user(db=db, user_id=user_id)
    return DeleteUserResponse.model_validate(response_service)
