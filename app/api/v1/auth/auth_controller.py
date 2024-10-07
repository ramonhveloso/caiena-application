from typing import Annotated

from fastapi import APIRouter, Depends, Security, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.auth.auth_repository import AuthRepository
from app.api.v1.auth.auth_schemas import (
    GetAuthMeResponse,
    PostForgotPasswordRequest,
    PostForgotPasswordResponse,
    PostLoginResponse,
    PostLogoutResponse,
    PostResetPasswordRequest,
    PostResetPasswordResponse,
    PostSignUpRequest,
    PostSignUpResponse,
    PutChangePasswordRequest,
    PutChangePasswordResponse,
)
from app.api.v1.auth.auth_service import AuthService
from app.middleware.dependencies import AuthUser, get_db, jwt_middleware

router = APIRouter()
auth_service = AuthService(AuthRepository())


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def post_signup(
    data: PostSignUpRequest, db: AsyncSession = Depends(get_db)
) -> PostSignUpResponse:
    response_service = await auth_service.create_user(db=db, data=data)
    return PostSignUpResponse.model_validate(response_service)


@router.post("/login")
async def post_login(
    data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
) -> PostLoginResponse:
    authenticated_user = await auth_service.authenticate_user(db=db, data=data)
    response_service = auth_service.create_access_token(authenticated_user)
    return PostLoginResponse.model_validate(response_service)


@router.post("/logout")
async def post_logout(
    authuser: Annotated[AuthUser, Security(jwt_middleware)],
    db: AsyncSession = Depends(get_db),
) -> PostLogoutResponse:
    response_service = await auth_service.logout(db=db, authuser=authuser)
    return PostLogoutResponse.model_validate(response_service)


@router.post("/forgot-password")
async def post_forgot_password(
    data: PostForgotPasswordRequest, db: AsyncSession = Depends(get_db)
) -> PostForgotPasswordResponse:
    response_service = await auth_service.forgot_password(db=db, data=data)
    return PostForgotPasswordResponse.model_validate(response_service)


@router.post("/reset-password")
async def post_reset_password(
    data: PostResetPasswordRequest, db: AsyncSession = Depends(get_db)
) -> PostResetPasswordResponse:
    response_service = await auth_service.reset_password(db=db, data=data)
    return PostResetPasswordResponse.model_validate(response_service)


@router.put("/change-password")
async def put_change_password(
    authuser: Annotated[AuthUser, Security(jwt_middleware)],
    data: PutChangePasswordRequest,
    db: AsyncSession = Depends(get_db),
) -> PutChangePasswordResponse:
    response_service = await auth_service.change_password(
        db=db, authuser=authuser, data=data
    )
    return PutChangePasswordResponse.model_validate(response_service)


@router.get("/me")
async def get_me(
    authuser: Annotated[AuthUser, Security(jwt_middleware)],
    db: AsyncSession = Depends(get_db),
) -> GetAuthMeResponse:
    response_service = await auth_service.get_authenticated_user(db=db, id=authuser.id)
    return GetAuthMeResponse.model_validate(response_service)
