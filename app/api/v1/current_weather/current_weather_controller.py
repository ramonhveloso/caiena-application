from typing import Annotated

from fastapi import APIRouter, Depends, Security, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.current_weather.current_weather_repository import (
    CurrentWeatherRepository,
)
from app.api.v1.current_weather.current_weather_schemas import (
    DeleteWeatherCurrentResponse,
    GetAllWeatherCurrentResponse,
    GetWeatherCurrentResponse,
    PutWeatherCurrentRequest,
    PutWeatherCurrentResponse,
)
from app.api.v1.current_weather.current_weather_service import CurrentWeatherService
from app.clients.http_client import HttpClient
from app.clients.open_weather.open_weather_client import OpenWeatherClient
from app.clients.open_weather.open_weather_schemas import CoordinatesRequest
from app.middleware.dependencies import AuthUser, get_db, jwt_middleware

router = APIRouter()
weather_service = CurrentWeatherService(
    CurrentWeatherRepository(), OpenWeatherClient(HttpClient())
)


@router.post("/coordinates", status_code=status.HTTP_201_CREATED)
async def post_weather_current_by_coordinates(
    authuser: Annotated[AuthUser, Security(jwt_middleware)],
    coordinates: CoordinatesRequest = Depends(),
    db: AsyncSession = Depends(get_db),
) -> GetWeatherCurrentResponse:
    response_service = await weather_service.post_current_weather_by_coordinates(
        authuser=authuser, db=db, coordinates=coordinates
    )
    return GetWeatherCurrentResponse.model_validate(response_service)


@router.post("/{city}", status_code=status.HTTP_201_CREATED)
async def post_weather_current_by_city(
    authuser: Annotated[AuthUser, Security(jwt_middleware)],
    city: str,
    db: AsyncSession = Depends(get_db),
) -> GetWeatherCurrentResponse:
    response_service = await weather_service.post_current_weather_by_city(
        authuser=authuser, db=db, city=city
    )
    return GetWeatherCurrentResponse.model_validate(response_service)


@router.get("/user/{user_id}")
async def get_weather_current_by_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
) -> GetAllWeatherCurrentResponse:
    response_service = await weather_service.get_all_current_weather_by_user(
        db=db, user_id=user_id
    )
    return GetAllWeatherCurrentResponse.model_validate(response_service)


@router.put("/{id}")
async def put_weather_current(
    id: int,
    data: PutWeatherCurrentRequest,
    authuser: Annotated[AuthUser, Security(jwt_middleware)],
    db: AsyncSession = Depends(get_db),
) -> PutWeatherCurrentResponse:
    response_service = await weather_service.update_current_weather(
        db=db, weather_id=id, data=data
    )
    return PutWeatherCurrentResponse.model_validate(response_service)


@router.delete("/{id}")
async def delete_weather_current(
    id: int,
    authuser: Annotated[AuthUser, Security(jwt_middleware)],
    db: AsyncSession = Depends(get_db),
) -> DeleteWeatherCurrentResponse:
    response_service = await weather_service.delete_current_weather(
        db=db, weather_id=id
    )
    return DeleteWeatherCurrentResponse.model_validate(response_service)
