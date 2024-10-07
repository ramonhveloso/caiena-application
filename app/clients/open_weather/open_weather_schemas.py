from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class CoordinatesRequest(BaseModel):
    latitude: float
    longitude: float


class WeatherDescription(BaseModel):
    main: str
    description: str

    class Config:
        from_attributes = True


class MainWeather(BaseModel):
    temp: float
    feels_like: float
    temp_min: float
    temp_max: float
    pressure: int
    humidity: int
    sea_level: Optional[int] = None
    grnd_level: Optional[int] = None

    class Config:
        from_attributes = True


class Wind(BaseModel):
    speed: float
    deg: int
    gust: Optional[float] = None

    class Config:
        from_attributes = True


class Clouds(BaseModel):
    all: int

    class Config:
        from_attributes = True


class Sys(BaseModel):
    country: str
    sunrise: int
    sunset: int

    class Config:
        from_attributes = True


class Coordinates(BaseModel):
    lon: float
    lat: float

    class Config:
        from_attributes = True


class GetCurrentWeatherResponse(BaseModel):
    coord: Coordinates
    weather: List[WeatherDescription]
    main: MainWeather
    visibility: Optional[int] = None
    wind: Wind
    clouds: Clouds
    dt: int
    sys: Sys
    timezone: int
    id: int
    name: str
    cod: int

    class Config:
        from_attributes = True


class MainSchema(BaseModel):
    temp: float
    feels_like: float
    temp_min: float
    temp_max: float
    pressure: int
    sea_level: Optional[int]
    grnd_level: Optional[int]
    humidity: int
    temp_kf: Optional[float]

    class Config:
        from_attributes = True


class WeatherSchema(BaseModel):
    id: int
    main: str
    description: str
    icon: str

    class Config:
        from_attributes = True


class CloudsSchema(BaseModel):
    all: int

    class Config:
        from_attributes = True


class WindSchema(BaseModel):
    speed: float
    deg: int
    gust: Optional[float]

    class Config:
        from_attributes = True


class SysSchema(BaseModel):
    pod: str

    class Config:
        from_attributes = True


class WeatherDataSchema(BaseModel):
    dt: datetime
    main: MainSchema
    weather: List[WeatherSchema]
    clouds: CloudsSchema
    wind: WindSchema
    visibility: Optional[int] = None
    pop: Optional[float]
    sys: SysSchema
    dt_txt: str

    class Config:
        from_attributes = True


class CityData(BaseModel):
    id: int
    name: str
    coord: Coordinates
    country: str
    population: int
    timezone: int
    sunrise: int
    sunset: int

    class Config:
        from_attributes = True


class WeatherForecastResponseSchema(BaseModel):
    cod: str
    message: int
    cnt: int
    list: List[WeatherDataSchema]
    city: CityData

    class Config:
        from_attributes = True
