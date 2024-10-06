from typing import List, Optional
from pydantic import BaseModel, condecimal
from datetime import datetime

from app.clients.open_weather.open_weather_schemas import GetForecastWeatherResponse
from app.database.models.forecast_weather import ForecastWeather


class PostWeatherForecastRequest(BaseModel):
    city: str
    forecast_temperature: float
    weather_description: str
    observation_datetime: Optional[datetime] = None
    user_id: int

    class Config:
        from_attributes = True

    @classmethod
    def model_validate(cls, data):
        if isinstance(data, cls):
            data = data.model_dump()
        return cls(**data)
    

class CoordinatesRequest(BaseModel):
    latitude: float
    longitude: float


class PostWeatherForecastResponse(BaseModel):
    id: int
    city: str
    forecast_temperature: float
    weather_description: str
    observation_datetime: datetime
    user_id: int

    class Config:
        from_attributes = True

    @classmethod
    def model_validate(cls, data):
        if isinstance(data, cls):
            data = data.model_dump()
        return cls(**data)


class GetWeatherForecastResponse(BaseModel): 
    id: int
    city: str
    latitude: float
    longitude: float
    date: datetime
    average_temperature: float
    min_temperature: float
    max_temperature: float
    weather_description: str
    humidity: float
    wind_speed: float
    user_id: int

    class Config:
        from_attributes = True

    @classmethod
    def model_validate(cls, data):
        if isinstance(data, cls):
            data = data.model_dump()
        return cls(**data)
    

class PutWeatherForecastRequest(BaseModel):
    id: int
    city: str
    latitude: float
    longitude: float
    date: datetime
    average_temperature: float
    min_temperature: float
    max_temperature: float
    weather_description: str
    humidity: float
    wind_speed: float
    user_id: int

    class Config:
        from_attributes = True


class PutWeatherForecastResponse(GetWeatherForecastResponse):
    pass


class DeleteWeatherForecastResponse(GetWeatherForecastResponse):
    pass


class CreateForecastWeatherRequest(BaseModel):
    city: str
    latitude: float
    longitude: float
    date: datetime
    average_temperature: float
    min_temperature: float
    max_temperature: float
    weather_description: str
    humidity: float
    wind_speed: float

    class Config:
        from_attributes = True

    @classmethod
    def model_validate(cls, data):
        if isinstance(data, cls):
            data = data.model_dump()
        return cls(**data)
    


class CreateForecastWeatherResponse(GetWeatherForecastResponse):
    pass
    

class GetAllWeatherForecastResponse(BaseModel):

    weathers: List[CreateForecastWeatherResponse]
