from datetime import datetime

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.current_weather.current_weather_repository import (
    CurrentWeatherRepository,
)
from app.api.v1.current_weather.current_weather_schemas import (
    CreateCurrentWeatherRequest,
    DeleteWeatherCurrentResponse,
    GetAllWeatherCurrentResponse,
    GetWeatherCurrentResponse,
    PutWeatherCurrentRequest,
    PutWeatherCurrentResponse,
)
from app.clients.open_weather.open_weather_client import OpenWeatherClient
from app.clients.open_weather.open_weather_schemas import CoordinatesRequest
from app.middleware.dependencies import AuthUser


class CurrentWeatherService:
    def __init__(
        self,
        current_weather_repository: CurrentWeatherRepository = Depends(),
        current_weather_client: OpenWeatherClient = Depends(),
    ):
        self.current_weather_repository = current_weather_repository
        self.open_weather_client = current_weather_client

    async def get_current_weather_by_coordinates(
        self, authuser: AuthUser, db: AsyncSession, coordinates: CoordinatesRequest
    ) -> GetWeatherCurrentResponse:
        response_client = (
            await self.open_weather_client.get_current_weather_by_coordinates(
                coordinates=coordinates
            )
        )
        current_weather = CreateCurrentWeatherRequest(**response_client.model_dump())

        weather = await self.current_weather_repository.create(
            db, authuser.id, current_weather
        )
        return GetWeatherCurrentResponse(
            id=int(weather.id),
            city=str(weather.city),
            latitude=float(weather.latitude),
            longitude=float(weather.longitude),
            current_temperature=float(weather.current_temperature),
            feels_like=float(weather.feels_like),
            temp_min=float(weather.temp_min),
            temp_max=float(weather.temp_max),
            pressure=int(weather.pressure),
            humidity=int(weather.humidity),
            visibility=int(weather.visibility),
            wind_speed=float(weather.wind_speed),
            wind_deg=int(weather.wind_deg),
            wind_gust=float(weather.wind_gust) if weather.wind_gust else None,
            cloudiness=int(weather.cloudiness),
            weather_description=str(weather.weather_description),
            observation_datetime=datetime.strptime(
                str(weather.observation_datetime), "%Y-%m-%d %H:%M:%S"
            ),
            sunrise=datetime.strptime(str(weather.sunrise), "%Y-%m-%d %H:%M:%S"),
            sunset=datetime.strptime(str(weather.sunset), "%Y-%m-%d %H:%M:%S"),
            user_id=int(weather.user_id),
        )

    async def get_current_weather_by_city(
        self, authuser: AuthUser, db: AsyncSession, city: str
    ) -> GetWeatherCurrentResponse:
        response_client = await self.open_weather_client.get_current_weather_by_city(
            city=city
        )
        current_weather = CreateCurrentWeatherRequest(**response_client.model_dump())

        weather = await self.current_weather_repository.create(
            db, authuser.id, current_weather
        )
        return GetWeatherCurrentResponse(
            id=int(weather.id),
            city=str(weather.city),
            latitude=float(weather.latitude),
            longitude=float(weather.longitude),
            current_temperature=float(weather.current_temperature),
            feels_like=float(weather.feels_like),
            temp_min=float(weather.temp_min),
            temp_max=float(weather.temp_max),
            pressure=int(weather.pressure),
            humidity=int(weather.humidity),
            visibility=int(weather.visibility),
            wind_speed=float(weather.wind_speed),
            wind_deg=int(weather.wind_deg),
            wind_gust=float(weather.wind_gust) if weather.wind_gust else None,
            cloudiness=int(weather.cloudiness),
            weather_description=str(weather.weather_description),
            observation_datetime=datetime.strptime(
                str(weather.observation_datetime), "%Y-%m-%d %H:%M:%S"
            ),
            sunrise=datetime.strptime(str(weather.sunrise), "%Y-%m-%d %H:%M:%S"),
            sunset=datetime.strptime(str(weather.sunset), "%Y-%m-%d %H:%M:%S"),
            user_id=int(weather.user_id),
        )

    async def get_all_current_weather_by_user(
        self, db: AsyncSession, user_id: int
    ) -> GetAllWeatherCurrentResponse:
        weathers = await self.current_weather_repository.get_all_weathers_by_user_id(
            db, user_id
        )
        if not weathers:
            raise HTTPException(status_code=404, detail="Weather not found")

        weathers_list = [
            GetWeatherCurrentResponse(
                id=int(weather.id),
                city=str(weather.city),
                latitude=float(weather.latitude),
                longitude=float(weather.longitude),
                current_temperature=float(weather.current_temperature),
                feels_like=float(weather.feels_like),
                temp_min=float(weather.temp_min),
                temp_max=float(weather.temp_max),
                pressure=int(weather.pressure),
                humidity=int(weather.humidity),
                visibility=int(weather.visibility),
                wind_speed=float(weather.wind_speed),
                wind_deg=int(weather.wind_deg),
                wind_gust=float(weather.wind_gust) if weather.wind_gust else None,
                cloudiness=int(weather.cloudiness),
                weather_description=str(weather.weather_description),
                observation_datetime=datetime.strptime(
                    str(weather.observation_datetime), "%Y-%m-%d %H:%M:%S"
                ),
                sunrise=datetime.strptime(str(weather.sunrise), "%Y-%m-%d %H:%M:%S"),
                sunset=datetime.strptime(str(weather.sunset), "%Y-%m-%d %H:%M:%S"),
                user_id=int(weather.user_id),
            )
            for weather in weathers
        ]
        return GetAllWeatherCurrentResponse(weathers=weathers_list)

    async def update_current_weather(
        self, db: AsyncSession, weather_id: int, data: PutWeatherCurrentRequest
    ) -> PutWeatherCurrentResponse:
        weather = await self.current_weather_repository.get_current_weather_by_id(
            db, weather_id
        )
        if not weather:
            raise HTTPException(status_code=404, detail="Weather not found")

        updated_weather = await self.current_weather_repository.update(
            db, weather, data
        )
        return PutWeatherCurrentResponse(
            message="Current Weather updated successfully",
            response=GetWeatherCurrentResponse(
                id=int(updated_weather.id),
                city=str(updated_weather.city),
                latitude=float(updated_weather.latitude),
                longitude=float(updated_weather.longitude),
                current_temperature=float(updated_weather.current_temperature),
                feels_like=float(updated_weather.feels_like),
                temp_min=float(updated_weather.temp_min),
                temp_max=float(updated_weather.temp_max),
                pressure=int(updated_weather.pressure),
                humidity=int(updated_weather.humidity),
                visibility=int(updated_weather.visibility),
                wind_speed=float(updated_weather.wind_speed),
                wind_deg=int(updated_weather.wind_deg),
                wind_gust=(
                    float(updated_weather.wind_gust) if weather.wind_gust else None
                ),
                cloudiness=int(updated_weather.cloudiness),
                weather_description=str(updated_weather.weather_description),
                observation_datetime=datetime.strptime(
                    str(updated_weather.observation_datetime), "%Y-%m-%d %H:%M:%S"
                ),
                sunrise=datetime.strptime(
                    str(updated_weather.sunrise), "%Y-%m-%d %H:%M:%S"
                ),
                sunset=datetime.strptime(
                    str(updated_weather.sunset), "%Y-%m-%d %H:%M:%S"
                ),
                user_id=int(updated_weather.user_id),
            ),
        )

    async def delete_current_weather(
        self, db: AsyncSession, weather_id: int
    ) -> DeleteWeatherCurrentResponse:
        weather = await self.current_weather_repository.get_current_weather_by_id(
            db, weather_id
        )
        if not weather:
            raise HTTPException(status_code=404, detail="Weather not found")

        try:
            await self.current_weather_repository.delete(db, weather.id)
        except Exception:
            raise HTTPException(status_code=409, detail="Error deleting weather")

        return DeleteWeatherCurrentResponse(
            message="Current Weather deleted successfully",
            response=GetWeatherCurrentResponse(
                id=int(weather.id),
                city=str(weather.city),
                latitude=float(weather.latitude),
                longitude=float(weather.longitude),
                current_temperature=float(weather.current_temperature),
                feels_like=float(weather.feels_like),
                temp_min=float(weather.temp_min),
                temp_max=float(weather.temp_max),
                pressure=int(weather.pressure),
                humidity=int(weather.humidity),
                visibility=int(weather.visibility),
                wind_speed=float(weather.wind_speed),
                wind_deg=int(weather.wind_deg),
                wind_gust=float(weather.wind_gust) if weather.wind_gust else None,
                cloudiness=int(weather.cloudiness),
                weather_description=str(weather.weather_description),
                observation_datetime=datetime.strptime(
                    str(weather.observation_datetime), "%Y-%m-%d %H:%M:%S"
                ),
                sunrise=datetime.strptime(str(weather.sunrise), "%Y-%m-%d %H:%M:%S"),
                sunset=datetime.strptime(str(weather.sunset), "%Y-%m-%d %H:%M:%S"),
                user_id=int(weather.user_id),
            ),
        )
