from typing import Annotated

from fastapi import APIRouter, Depends, Security, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.forecasts_weather.forecast_weather_repository import (
    ForecastWeatherRepository,
)
from app.api.v1.forecasts_weather.forecast_weather_schemas import (
    DeleteWeatherForecastResponse,
    GetAllWeatherForecastResponse,
    PutWeatherForecastRequest,
    PutWeatherForecastResponse,
)
from app.api.v1.forecasts_weather.forecast_weather_service import ForecastWeatherService
from app.clients.http_client import HttpClient
from app.clients.open_weather.open_weather_client import OpenWeatherClient
from app.clients.open_weather.open_weather_schemas import CoordinatesRequest
from app.middleware.dependencies import AuthUser, get_db, jwt_middleware

router = APIRouter()
weather_service = ForecastWeatherService(
    ForecastWeatherRepository(), OpenWeatherClient(HttpClient())
)


@router.post("/coordinates", status_code=status.HTTP_201_CREATED)
async def post_weather_forecast_by_coordinates(
    authuser: Annotated[AuthUser, Security(jwt_middleware)],
    coordinates: CoordinatesRequest = Depends(),
    db: AsyncSession = Depends(get_db),
) -> GetAllWeatherForecastResponse:
    response_service = await weather_service.post_forecast_weather_by_coordinates(
        authuser=authuser, db=db, coordinates=coordinates
    )
    return GetAllWeatherForecastResponse.model_validate(response_service)


@router.post("/{city}", status_code=status.HTTP_201_CREATED)
async def post_weather_forecast_by_city(
    authuser: Annotated[AuthUser, Security(jwt_middleware)],
    city: str,
    db: AsyncSession = Depends(get_db),
) -> GetAllWeatherForecastResponse:
    response_service = await weather_service.post_forecast_weather_by_city(
        authuser=authuser, db=db, city=city
    )
    return GetAllWeatherForecastResponse.model_validate(response_service)


@router.get("/user/{user_id}")
async def get_weather_forecast_by_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
) -> GetAllWeatherForecastResponse:
    response_service = await weather_service.get_all_forecast_weather_by_user(
        db=db, user_id=user_id
    )
    return GetAllWeatherForecastResponse.model_validate(response_service)


@router.put("/{id}")
async def put_weather_forecast(
    id: int,
    data: PutWeatherForecastRequest,
    authuser: Annotated[AuthUser, Security(jwt_middleware)],
    db: AsyncSession = Depends(get_db),
) -> PutWeatherForecastResponse:
    response_service = await weather_service.update_forecast_weather(
        db=db, weather_id=id, data=data
    )
    return PutWeatherForecastResponse.model_validate(response_service)


@router.delete("/{id}")
async def delete_weather_forecast(
    id: int,
    authuser: Annotated[AuthUser, Security(jwt_middleware)],
    db: AsyncSession = Depends(get_db),
) -> DeleteWeatherForecastResponse:
    response_service = await weather_service.delete_forecast_weather(
        db=db, weather_id=id
    )
    return DeleteWeatherForecastResponse.model_validate(response_service)
