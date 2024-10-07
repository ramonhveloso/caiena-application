from typing import Annotated

from fastapi import APIRouter, Depends, Security, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.current_weather.current_weather_repository import CurrentWeatherRepository
from app.api.v1.forecasts_weather.forecast_weather_repository import ForecastWeatherRepository
from app.api.v1.gist_comments.gist_comment_repository import GistCommentRepository
from app.api.v1.gist_comments.gist_comment_schemas import (
    CoordinatesRequest,
    DeleteGistCommentResponse,
    GetAllGistCommentResponse,
    GistCommentResponse,
    PutGistCommentRequest,
    PutGistCommentResponse,
)
from app.api.v1.gist_comments.gist_comment_service import CommentService
from app.clients.github.github_client import GitHubClient
from app.clients.http_client import HttpClient
from app.clients.open_weather.open_weather_client import OpenWeatherClient
from app.middleware.dependencies import AuthUser, get_db, jwt_middleware

router = APIRouter()
gist_comment_service = CommentService(
    GistCommentRepository(), 
    CurrentWeatherRepository(),
    ForecastWeatherRepository(),
    OpenWeatherClient(HttpClient()),
    GitHubClient()
)

@router.post("/coordinates", status_code=status.HTTP_201_CREATED)
async def post_gist_comment_by_city(
    authuser: Annotated[AuthUser, Security(jwt_middleware)],
    coordinates: CoordinatesRequest = Depends(),
    db: AsyncSession = Depends(get_db),
) -> GistCommentResponse:
    response_service = await gist_comment_service.post_gist_comment_by_coordinates(
        authuser=authuser, db=db, coordinates=coordinates
    )
    return GistCommentResponse.model_validate(response_service)

@router.post("/{city}", status_code=status.HTTP_201_CREATED)
async def get_gist_comment_by_city(
    authuser: Annotated[AuthUser, Security(jwt_middleware)],
    city: str,
    db: AsyncSession = Depends(get_db),
) -> GistCommentResponse:
    response_service = await gist_comment_service.post_gist_comment_by_city(authuser=authuser, db=db, city=city)
    return GistCommentResponse.model_validate(response_service)

@router.get("/user/{user_id}")
async def get_gist_comments_by_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
) -> GetAllGistCommentResponse:
    response_service = await gist_comment_service.get_all_gist_comment_by_user(db=db, user_id=user_id)
    return GetAllGistCommentResponse.model_validate(response_service)

@router.put("/{comment_id}")
async def put_gist_comment(
    comment_id: int,
    data: PutGistCommentRequest,
    authuser: Annotated[AuthUser, Security(jwt_middleware)],
    db: AsyncSession = Depends(get_db),
) -> PutGistCommentResponse:
    response_service = await gist_comment_service.update_gist_comment(
        db=db, comment_id=comment_id, data=data
    )
    return PutGistCommentResponse.model_validate(response_service)

@router.delete("/{comment_id}")
async def delete_gist_comment(
    comment_id: int,
    authuser: Annotated[AuthUser, Security(jwt_middleware)],
    db: AsyncSession = Depends(get_db),
) -> DeleteGistCommentResponse:
    response_service = await gist_comment_service.delete_gist_comment(db=db, comment_id=comment_id)
    return DeleteGistCommentResponse.model_validate(response_service)
