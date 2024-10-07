from datetime import datetime
from typing import List

from pydantic import BaseModel


class CoordinatesRequest(BaseModel):
    latitude: float
    longitude: float


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


class PutWeatherForecastResponse(BaseModel):
    message: str
    response: GetWeatherForecastResponse


class DeleteWeatherForecastResponse(BaseModel):
    message: str
    response: GetWeatherForecastResponse



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


class PutWeatherForecastRequest(CreateForecastWeatherRequest):
    id: int


class CreateForecastWeatherResponse(GetWeatherForecastResponse):
    pass


class GetAllWeatherForecastResponse(BaseModel):

    weathers: List[CreateForecastWeatherResponse]
