from app.api.v1.current_weather.current_weather_schemas import CoordinatesRequest
from app.clients.http_client import HttpClient
from app.clients.open_weather.open_weather_schemas import (
    GetCurrentWeatherResponse,
    WeatherForecastResponseSchema,
)
from app.config import Environment
from app.utils.env_vars import validate_variables


class OpenWeatherClient:
    def __init__(self, http_client: HttpClient) -> None:
        environment = validate_variables(Environment)
        self.current_weather_url = f"{str(environment.OPEN_WEATHER_URL)}weather"
        self.forrest_weather_url = f"{str(environment.OPEN_WEATHER_URL)}forecast"
        self.secret_key_open_weather = environment.SECRET_KEY_OPEN_WEATHER
        self.http_client = http_client

    async def get_current_weather_by_coordinates(
        self, coordinates: CoordinatesRequest
    ) -> GetCurrentWeatherResponse:
        response = await self.http_client.make_request(
            self.current_weather_url,
            "GET",
            params={
                "lat": coordinates.latitude,
                "lon": coordinates.longitude,
                "appid": self.secret_key_open_weather,
                "units": "metric",
                "lang": "pt_br",
            },
        )
        return GetCurrentWeatherResponse(**response.json())

    async def get_current_weather_by_city(self, city: str) -> GetCurrentWeatherResponse:
        f"{str(self.base_url)}weather"
        response = await self.http_client.make_request(
            self.current_weather_url,
            "GET",
            params={
                "q": city,
                "appid": self.secret_key_open_weather,
                "units": "metric",
                "lang": "pt_br",
            },
        )
        return GetCurrentWeatherResponse(**response.json())

    async def get_forecast_weather_by_coordinates(
        self, coordinates: CoordinatesRequest
    ) -> WeatherForecastResponseSchema:
        response = await self.http_client.make_request(
            self.forrest_weather_url,
            "GET",
            params={
                "lat": coordinates.latitude,
                "lon": coordinates.longitude,
                "appid": self.secret_key_open_weather,
                "units": "metric",
                "lang": "pt_br",
            },
        )
        return WeatherForecastResponseSchema(**response.json())

    async def get_forecast_weather_daily_by_coordinates(
        self, coordinates: CoordinatesRequest
    ) -> WeatherForecastResponseSchema:
        response = await self.http_client.make_request(
            self.forrest_weather_daily_url,
            "GET",
            params={
                "lat": coordinates.latitude,
                "lon": coordinates.longitude,
                "appid": self.secret_key_open_weather,
                "units": "metric",
                "lang": "pt_br",
            },
        )
        return WeatherForecastResponseSchema(**response.json())

    async def get_forecast_weather_by_city(
        self, city: str
    ) -> WeatherForecastResponseSchema:
        response = await self.http_client.make_request(
            self.forrest_weather_url,
            "GET",
            params={
                "q": city,
                "appid": self.secret_key_open_weather,
                "units": "metric",
                "lang": "pt_br",
            },
        )
        return WeatherForecastResponseSchema(**response.json())
