from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from app.clients.open_weather.open_weather_schemas import GetCurrentWeatherResponse
from app.database.models.current_weather import CurrentWeather
    

class CoordinatesRequest(BaseModel):
    latitude: float
    longitude: float


class GetWeatherCurrentResponse(BaseModel):
    id: int
    city: str
    latitude: float
    longitude: float
    current_temperature: float
    feels_like: float
    temp_min: float
    temp_max: float
    pressure: int
    humidity: int
    visibility: int
    wind_speed: float
    wind_deg: int
    wind_gust: Optional[float] = None
    cloudiness: int
    weather_description: str
    observation_datetime: datetime
    sunrise: datetime
    sunset: datetime
    user_id: int

    class Config:
        from_attributes = True

    @classmethod
    def model_validate(cls, data):
        if isinstance(data, cls):
            data = data.model_dump()
        return cls(**data)
    
class GetAllWeatherCurrentResponse(BaseModel):
    weathers: List[GetWeatherCurrentResponse]


class PutWeatherCurrentRequest(GetWeatherCurrentResponse):
    pass


class PutWeatherCurrentResponse(GetWeatherCurrentResponse):
    pass


class DeleteWeatherCurrentResponse(GetWeatherCurrentResponse):
    pass

class CreateCurrentWeatherRequest(GetCurrentWeatherResponse):
    pass

class CreateCurrentWeatherResponse(CurrentWeather):
    pass
    