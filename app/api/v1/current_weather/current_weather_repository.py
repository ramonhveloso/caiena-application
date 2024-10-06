from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.current_weather.current_weather_schemas import (
    CreateCurrentWeatherRequest,
    CreateCurrentWeatherResponse,
    PutWeatherCurrentRequest,
)
from app.database.models.current_weather import CurrentWeather


class CurrentWeatherRepository:
    async def create(
        self,
        db: AsyncSession,
        user_id: int,
        current_weather: CreateCurrentWeatherRequest,
    ) -> CreateCurrentWeatherResponse:
        current_weather_instance = CurrentWeather(
            city=current_weather.name,
            latitude=current_weather.coord.lat,
            longitude=current_weather.coord.lon,
            current_temperature=current_weather.main.temp,
            feels_like=current_weather.main.feels_like,
            temp_min=current_weather.main.temp_min,
            temp_max=current_weather.main.temp_max,
            pressure=current_weather.main.pressure,
            humidity=current_weather.main.humidity,
            visibility=current_weather.visibility,
            wind_speed=current_weather.wind.speed,
            wind_deg=current_weather.wind.deg,
            wind_gust=current_weather.wind.gust,
            cloudiness=current_weather.clouds.all,
            weather_description=current_weather.weather[0].description,
            observation_datetime=datetime.fromtimestamp(current_weather.dt),
            sunrise=datetime.fromtimestamp(current_weather.sys.sunrise),
            sunset=datetime.fromtimestamp(current_weather.sys.sunset),
            user_id=user_id,
        )

        db.add(current_weather_instance)
        db.commit()
        db.refresh(current_weather_instance)

        return CreateCurrentWeatherResponse(
            id=current_weather_instance.id,
            city=current_weather_instance.city,
            latitude=current_weather_instance.latitude,
            longitude=current_weather_instance.longitude,
            current_temperature=current_weather_instance.current_temperature,
            feels_like=current_weather_instance.feels_like,
            temp_min=current_weather_instance.temp_min,
            temp_max=current_weather_instance.temp_max,
            pressure=current_weather_instance.pressure,
            humidity=current_weather_instance.humidity,
            visibility=current_weather_instance.visibility,
            wind_speed=current_weather_instance.wind_speed,
            wind_deg=current_weather_instance.wind_deg,
            wind_gust=current_weather_instance.wind_gust,
            cloudiness=current_weather_instance.cloudiness,
            weather_description=current_weather_instance.weather_description,
            observation_datetime=current_weather_instance.observation_datetime,
            sunrise=current_weather_instance.sunrise,
            sunset=current_weather_instance.sunset,
            user_id=current_weather_instance.user_id,
        )

    async def get_by_city(self, db: AsyncSession, city: str) -> list[CurrentWeather]:
        return db.query(CurrentWeather).filter(CurrentWeather.city == city).all()

    async def get_all_weathers_by_user_id(self, db: AsyncSession, user_id: int):
        return db.query(CurrentWeather).filter(CurrentWeather.user_id == user_id).all()

    async def get_current_weather_by_id(self, db: AsyncSession, weather_id: int):
        return db.query(CurrentWeather).filter(CurrentWeather.id == weather_id).first()

    async def update(
        self,
        db: AsyncSession,
        current_weather: CurrentWeather,
        data: PutWeatherCurrentRequest,
    ):
        current_weather.city = data.city if data.city else current_weather.city  # type: ignore
        current_weather.latitude = (
            data.latitude if data.latitude else current_weather.latitude
        )
        current_weather.longitude = (
            data.longitude if data.longitude else current_weather.longitude
        )
        current_weather.current_temperature = (
            data.current_temperature
            if data.current_temperature
            else current_weather.current_temperature
        )
        current_weather.feels_like = (
            data.feels_like if data.feels_like else current_weather.feels_like
        )
        current_weather.temp_min = (
            data.temp_min if data.temp_min else current_weather.temp_min
        )
        current_weather.temp_max = (
            data.temp_max if data.temp_max else current_weather.temp_max
        )
        current_weather.pressure = (
            data.pressure if data.pressure else current_weather.pressure
        )
        current_weather.humidity = (
            data.humidity if data.humidity else current_weather.humidity
        )
        current_weather.visibility = (
            data.visibility if data.visibility else current_weather.visibility
        )
        current_weather.wind_speed = (
            data.wind_speed if data.wind_speed else current_weather.wind_speed
        )
        current_weather.wind_deg = (
            data.wind_deg if data.wind_deg else current_weather.wind_deg
        )
        current_weather.wind_gust = (
            data.wind_gust if data.wind_gust else current_weather.wind_gust
        )
        current_weather.cloudiness = (
            data.cloudiness if data.cloudiness else current_weather.cloudiness
        )
        current_weather.weather_description = (
            data.weather_description
            if data.weather_description
            else current_weather.weather_description
        )
        current_weather.observation_datetime = (
            data.observation_datetime
            if data.observation_datetime
            else current_weather.observation_datetime
        )
        current_weather.sunrise = (
            data.sunrise if data.sunrise else current_weather.sunrise
        )
        current_weather.sunset = data.sunset if data.sunset else current_weather.sunset
        current_weather.user_id = (
            data.user_id if data.user_id else current_weather.user_id
        )
        db.commit()
        db.refresh(current_weather)
        return current_weather

    async def delete(self, db: AsyncSession, weather_id: int):
        weather_entry = (
            db.query(CurrentWeather).filter(CurrentWeather.id == weather_id).first()
        )
        if weather_entry:
            db.delete(weather_entry)
            db.commit()
