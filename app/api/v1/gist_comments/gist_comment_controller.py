from typing import Annotated

from fastapi import APIRouter, Depends, Security
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.gist_comments.gist_comment_repository import GistCommentRepository
from app.api.v1.gist_comments.gist_comment_schemas import (
    CoordinatesRequest,
    GistCommentResponse, 
)
from app.api.v1.gist_comments.gist_comment_service import CommentService
from app.clients.http_client import HttpClient
from app.clients.open_weather.open_weather_client import OpenWeatherClient
from app.middleware.dependencies import AuthUser, get_db, jwt_middleware

router = APIRouter()
weather_service = CommentService(GistCommentRepository(), OpenWeatherClient(HttpClient()))


# Obter clima atual
@router.post("/current/coordinates")
async def post_weather_current_by_city(
    authuser: Annotated[AuthUser, Security(jwt_middleware)],
    coordinates: CoordinatesRequest = Depends(),
    db: AsyncSession = Depends(get_db),
) -> GistCommentResponse:
    response_service = await weather_service.post_gist_comment_by_coordinates(authuser=authuser, db=db, coordinates=coordinates)
    return GistCommentResponse.model_validate(response_service)

# # Obter clima atual
# @router.post("/current/{city}")
# async def get_weather_current_by_city(
#     authuser: Annotated[AuthUser, Security(jwt_middleware)],
#     city: str,
#     db: AsyncSession = Depends(get_db),
# ) -> GetWeatherCurrentResponse:
#     response_service = await weather_service.get_gist_comment_by_city(authuser=authuser, db=db, city=city)
#     return GetWeatherCurrentResponse.model_validate(response_service)


# # Obter climas cadastrados por usuário
# @router.get("/current/user/{user_id}")
# async def get_weather_current_by_user(
#     user_id: int,
#     db: AsyncSession = Depends(get_db),
# ) -> GetAllWeatherCurrentResponse:
#     response_service = await weather_service.get_all_gist_comment_by_user(db=db, user_id=user_id)
#     return GetAllWeatherCurrentResponse.model_validate(response_service)


# # Atualizar clima atual
# @router.put("/current/{id}")
# async def put_weather_current(
#     id: int,
#     data: PutWeatherCurrentRequest,
#     authuser: Annotated[AuthUser, Security(jwt_middleware)],
#     db: AsyncSession = Depends(get_db),
# ) -> PutWeatherCurrentResponse:
#     response_service = await weather_service.update_gist_comment(
#         db=db, weather_id=id, data=data
#     )   
#     return PutWeatherCurrentResponse.model_validate(response_service)


# # Excluir clima atual
# @router.delete("/current/{id}")
# async def delete_weather_current(
#     id: int,
#     authuser: Annotated[AuthUser, Security(jwt_middleware)],
#     db: AsyncSession = Depends(get_db),
# ) -> DeleteWeatherCurrentResponse:
#     response_service = await weather_service.delete_gist_comment(db=db, weather_id=id)
#     return DeleteWeatherCurrentResponse.model_validate(response_service)
