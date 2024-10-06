from datetime import datetime

from pydantic import BaseModel


class CreateGistCommentRequest(BaseModel):
    city: str
    current_temperature: float
    weather_description: str
    forecast_day_1_date: str
    forecast_day_1_temperature: float
    forecast_day_2_date: str
    forecast_day_2_temperature: float
    forecast_day_3_date: str
    forecast_day_3_temperature: float
    forecast_day_4_date: str
    forecast_day_4_temperature: float
    forecast_day_5_date: str
    forecast_day_5_temperature: float

    class Config:
        from_attributes = True


class GistCommentResponse(CreateGistCommentRequest):
    id: int
    comment_date: datetime


class CoordinatesRequest(BaseModel):
    latitude: float
    longitude: float
