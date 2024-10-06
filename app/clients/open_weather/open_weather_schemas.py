from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional

class WeatherDescription(BaseModel):
    main: str
    description: str

class MainWeather(BaseModel):
    temp: float
    feels_like: float
    temp_min: float
    temp_max: float
    pressure: int
    humidity: int
    sea_level: Optional[int] = None
    grnd_level: Optional[int] = None

class Wind(BaseModel):
    speed: float
    deg: int
    gust: Optional[float] = None

class Clouds(BaseModel):
    all: int

class Sys(BaseModel):
    country: str
    sunrise: int
    sunset: int

class Coordinates(BaseModel):
    lon: float
    lat: float


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

class GetForecastWeatherResponse(BaseModel):
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

class WeatherSchema(BaseModel):
    id: int
    main: str
    description: str
    icon: str

class CloudsSchema(BaseModel):
    all: int

class WindSchema(BaseModel):
    speed: float
    deg: int
    gust: Optional[float]

class SysSchema(BaseModel):
    pod: str

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


class CityData(BaseModel):
    id: int
    name: str
    coord: Coordinates
    country: str
    population: int
    timezone: int
    sunrise: int
    sunset: int


class WeatherForecastResponseSchema(BaseModel):
    cod: str
    message: int
    cnt: int
    list: List[WeatherDataSchema]
    city: CityData

    class Config:
        from_attributes = True
