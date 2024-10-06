from datetime import datetime, timezone
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.forecasts_weather.forecast_weather_repository import ForecastWeatherRepository

from app.api.v1.forecasts_weather.forecast_weather_schemas import CoordinatesRequest, CreateForecastWeatherRequest, DeleteWeatherForecastResponse, GetAllWeatherForecastResponse, GetWeatherForecastResponse, PutWeatherForecastRequest, PutWeatherForecastResponse
from app.clients.open_weather.open_weather_client import OpenWeatherClient
from app.clients.open_weather.open_weather_schemas import GetForecastWeatherResponse
from app.middleware.dependencies import AuthUser


class ForecastWeatherService:
    def __init__(self, forecast_weather_repository: ForecastWeatherRepository = Depends(),
        forecast_weather_client: OpenWeatherClient = Depends()):
        self.forecast_weather_repository = forecast_weather_repository
        self.open_weather_client = forecast_weather_client

    async def get_forecast_weather_by_coordinates(
        self, authuser: AuthUser, db: AsyncSession, coordinates: CoordinatesRequest
    ) -> GetAllWeatherForecastResponse:
        response_client = await self.open_weather_client.get_forecast_weather_by_coordinates(coordinates=coordinates)
        city = response_client.city.name
        latitude = response_client.city.coord.lat
        longitude = response_client.city.coord.lon
        list_wather = []
        for weather_data in response_client.list:
            forecast_weather = CreateForecastWeatherRequest(
                city=city,
                latitude=latitude,
                longitude=longitude,
                date=weather_data.dt,
                average_temperature=weather_data.main.temp,
                min_temperature=weather_data.main.temp_min,
                max_temperature=weather_data.main.temp_max,
                weather_description=weather_data.weather[0].description,
                humidity=weather_data.main.humidity,
                wind_speed=weather_data.wind.speed
            )
            response_repository = await self.forecast_weather_repository.create(db, authuser.id, forecast_weather)    
            list_wather.append(response_repository)    
        return GetAllWeatherForecastResponse(weathers=list_wather)
    
    async def get_forecast_weather_daily_by_coordinates(
        self, authuser: AuthUser, db: AsyncSession, coordinates: CoordinatesRequest
    ) -> GetAllWeatherForecastResponse:
        response_client = await self.open_weather_client.get_forecast_weather_daily_by_coordinates(coordinates=coordinates)
        city = response_client.city.name
        latitude = response_client.city.coord.lat
        longitude = response_client.city.coord.lon
        list_wather = []
        for weather_data in response_client.list:
            forecast_weather = CreateForecastWeatherRequest(
                city=city,
                latitude=latitude,
                longitude=longitude,
                date=weather_data.dt,
                average_temperature=weather_data.main.temp,
                min_temperature=weather_data.main.temp_min,
                max_temperature=weather_data.main.temp_max,
                weather_description=weather_data.weather[0].description,
                humidity=weather_data.main.humidity,
                wind_speed=weather_data.wind.speed
            )
            response_repository = await self.forecast_weather_repository.create(db, authuser.id, forecast_weather)    
            list_wather.append(response_repository)    
        return GetAllWeatherForecastResponse(weathers=list_wather)

    async def get_forecast_weather_by_city(
        self, authuser: AuthUser, db: AsyncSession, city: str
    ) -> GetAllWeatherForecastResponse:
        response_client = await self.open_weather_client.get_forecast_weather_by_city(city=city)
        city = response_client.city.name
        latitude = response_client.city.coord.lat
        longitude = response_client.city.coord.lon
        list_wather = []
        for weather_data in response_client.list:
            forecast_weather = CreateForecastWeatherRequest(
                city=city,
                latitude=latitude,
                longitude=longitude,
                date=weather_data.dt,
                average_temperature=weather_data.main.temp,
                min_temperature=weather_data.main.temp_min,
                max_temperature=weather_data.main.temp_max,
                weather_description=weather_data.weather[0].description,
                humidity=weather_data.main.humidity,
                wind_speed=weather_data.wind.speed
            )
            response_repository = await self.forecast_weather_repository.create(db, authuser.id, forecast_weather)    
            list_wather.append(response_repository)    
        return GetAllWeatherForecastResponse(weathers=list_wather)
    
    async def get_all_forecast_weather_by_user(
        self, db: Session, user_id: int
    ) -> GetAllWeatherForecastResponse:
        weathers = await self.forecast_weather_repository.get_all_weathers_by_user_id(db, user_id)
        weathers_list = [
            GetWeatherForecastResponse(
                id=int(weather.id), 
                city=str(weather.city),
                latitude=float(weather.latitude),
                longitude=float(weather.longitude),
                date=datetime.strptime(str(weather.date), '%Y-%m-%d %H:%M:%S'),
                average_temperature=float(weather.average_temperature),
                min_temperature=float(weather.min_temperature),
                max_temperature=float(weather.max_temperature),
                weather_description=str(weather.weather_description),    
                humidity=int(weather.humidity),
                wind_speed=float(weather.wind_speed),
                user_id=int(weather.user_id)
            )
            for weather in weathers
        ]
        return GetAllWeatherForecastResponse(weathers=weathers_list)

    async def update_forecast_weather(
        self, db: Session, weather_id: int, data: PutWeatherForecastRequest
    ) -> PutWeatherForecastResponse:
        weather = await self.forecast_weather_repository.get_forecast_weather_by_id(db, weather_id)
        if not weather:
            raise HTTPException(status_code=404, detail="Weather not found")
        
        updated_weather = await self.forecast_weather_repository.update(db, weather, data)
        return PutWeatherForecastResponse(
            id=int(updated_weather.id), 
            city=str(updated_weather.city),
            latitude=float(updated_weather.latitude),
            longitude=float(updated_weather.longitude),
            date=datetime.strptime(str(updated_weather.date), '%Y-%m-%d %H:%M:%S'),
            average_temperature=float(updated_weather.average_temperature),
            min_temperature=float(updated_weather.min_temperature),
            max_temperature=float(updated_weather.max_temperature),
            weather_description=str(updated_weather.weather_description),
            humidity=int(updated_weather.humidity),
            wind_speed=float(updated_weather.wind_speed),
            user_id=int(updated_weather.user_id)
        )

    async def delete_forecast_weather(
        self, db: Session, weather_id: int
    ) -> DeleteWeatherForecastResponse:
        weather = await self.forecast_weather_repository.get_forecast_weather_by_id(db, weather_id)
        if not weather:
            raise HTTPException(status_code=404, detail="Weather not found")
        
        # Excluir registro de clima atual
        await self.forecast_weather_repository.delete(db, weather.id)
        return DeleteWeatherForecastResponse(
            id=int(weather.id), 
            city=str(weather.city),
            latitude=float(weather.latitude),
            longitude=float(weather.longitude),
            date=datetime.strptime(str(weather.date), '%Y-%m-%d %H:%M:%S'),
            average_temperature=float(weather.average_temperature),
            min_temperature=float(weather.min_temperature),
            max_temperature=float(weather.max_temperature),
            weather_description=str(weather.weather_description),
            humidity=int(weather.humidity),
            wind_speed=float(weather.wind_speed),
            user_id=int(weather.user_id)
        )
