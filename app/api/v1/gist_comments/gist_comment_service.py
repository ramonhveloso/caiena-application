import pandas as pd
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.current_weather.current_weather_repository import (
    CurrentWeatherRepository,
)
from app.api.v1.current_weather.current_weather_schemas import (
    CreateCurrentWeatherRequest,
)
from app.api.v1.forecasts_weather.forecast_weather_repository import (
    ForecastWeatherRepository,
)
from app.api.v1.forecasts_weather.forecast_weather_schemas import (
    CreateForecastWeatherRequest,
)
from app.api.v1.gist_comments.gist_comment_repository import GistCommentRepository
from app.api.v1.gist_comments.gist_comment_schemas import (
    CreateGistCommentRequest,
    DeleteGistCommentResponse,
    GetAllGistCommentResponse,
    GistCommentResponse,
    PutGistCommentRequest,
    PutGistCommentResponse,
)
from app.clients.github.github_client import GitHubClient
from app.clients.open_weather.open_weather_client import OpenWeatherClient
from app.clients.open_weather.open_weather_schemas import CoordinatesRequest
from app.middleware.dependencies import AuthUser


class CommentService:
    def __init__(
        self,
        gist_comment_repository: GistCommentRepository = Depends(),
        current_weather_repository: CurrentWeatherRepository = Depends(),
        forecast_weather_repository: ForecastWeatherRepository = Depends(),
        open_weather_client: OpenWeatherClient = Depends(),
        github_client: GitHubClient = Depends(),
    ):
        self.gist_comment_repository = gist_comment_repository
        self.current_weather_repository = current_weather_repository
        self.forecast_weather_repository = forecast_weather_repository
        self.open_weather_client = open_weather_client
        self.github_client = github_client

    def generate_comment(self, data: CreateGistCommentRequest) -> str:
        comment = (
            f"**Relatório do clima para {data.city}:**\n"
            f"Localização: Latitude {round(data.latitude, 1)}, Longitude {round(data.longitude, 1)}\n"
            f"Temperatura atual: {round(data.current_temperature, 1)}°C\n"
            f"Descrição do clima: {data.weather_description}\n\n"
            f"**Previsão para os próximos 5 dias:**\n"
            f"- {data.forecast_day_1_date}: {round(data.forecast_day_1_temperature, 1)}°C\n"
            f"- {data.forecast_day_2_date}: {round(data.forecast_day_2_temperature, 1)}°C\n"
            f"- {data.forecast_day_3_date}: {round(data.forecast_day_3_temperature, 1)}°C\n"
            f"- {data.forecast_day_4_date}: {round(data.forecast_day_4_temperature, 1)}°C\n"
            f"- {data.forecast_day_5_date}: {round(data.forecast_day_5_temperature, 1)}°C\n"
        )
        return comment

    async def post_gist_comment_by_coordinates(
        self, authuser: AuthUser, db: AsyncSession, coordinates: CoordinatesRequest
    ) -> GistCommentResponse:
        current_weather_response_client = (
            await self.open_weather_client.get_current_weather_by_coordinates(
                coordinates=coordinates
            )
        )
        if not current_weather_response_client:
            raise HTTPException(status_code=404, detail="Current Weather not found")

        current_weather = CreateCurrentWeatherRequest(
            **current_weather_response_client.model_dump()
        )

        current_weather_response_repository = (
            await self.current_weather_repository.create(
                db, authuser.id, current_weather
            )
        )

        forecast_weather_response_client = (
            await self.open_weather_client.get_forecast_weather_by_coordinates(
                coordinates=coordinates
            )
        )
        if not forecast_weather_response_client:
            raise HTTPException(status_code=404, detail="Forecast Weather not found")

        city = forecast_weather_response_client.city.name
        latitude = forecast_weather_response_client.city.coord.lat
        longitude = forecast_weather_response_client.city.coord.lon
        list_forecast_wather = []
        for weather_data in forecast_weather_response_client.list:
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
                wind_speed=weather_data.wind.speed,
            )
            forecast_weather_response_repository = (
                await self.forecast_weather_repository.create(
                    db, authuser.id, forecast_weather
                )
            )
            list_forecast_wather.append(
                forecast_weather_response_repository.model_dump()
            )

        df = pd.DataFrame(list_forecast_wather)
        df["date_only"] = df["date"].dt.date
        daily_avg_temp = (
            df.groupby("date_only")["average_temperature"].mean().reset_index()
        )
        next_5_days = daily_avg_temp.head(5)

        gist_comment = CreateGistCommentRequest(
            city=city,
            latitude=latitude,
            longitude=longitude,
            current_temperature=float(
                current_weather_response_repository.current_temperature
            ),
            weather_description=str(
                current_weather_response_repository.weather_description
            ),
            forecast_day_1_date=str(next_5_days["date_only"].iloc[0]),
            forecast_day_1_temperature=next_5_days["average_temperature"].iloc[0],
            forecast_day_2_date=str(next_5_days["date_only"].iloc[1]),
            forecast_day_2_temperature=next_5_days["average_temperature"].iloc[1],
            forecast_day_3_date=str(next_5_days["date_only"].iloc[2]),
            forecast_day_3_temperature=next_5_days["average_temperature"].iloc[2],
            forecast_day_4_date=str(next_5_days["date_only"].iloc[3]),
            forecast_day_4_temperature=next_5_days["average_temperature"].iloc[3],
            forecast_day_5_date=str(next_5_days["date_only"].iloc[4]),
            forecast_day_5_temperature=next_5_days["average_temperature"].iloc[4],
        )

        gist_response = await self.github_client.create_gist_comment(
            comment=self.generate_comment(data=gist_comment)
        )

        gist_comment_response_repository = await self.gist_comment_repository.create(
            db, authuser.id, gist_response["comment_id"], gist_comment
        )

        return GistCommentResponse(**gist_comment_response_repository.model_dump())

    async def post_gist_comment_by_city(
        self, authuser: AuthUser, db: AsyncSession, city: str
    ) -> GistCommentResponse:
        current_weather_response_client = (
            await self.open_weather_client.get_current_weather_by_city(city=city)
        )
        if not current_weather_response_client:
            raise HTTPException(status_code=404, detail="Current Weather not found")

        current_weather = CreateCurrentWeatherRequest(
            **current_weather_response_client.model_dump()
        )

        current_weather_response_repository = (
            await self.current_weather_repository.create(
                db, authuser.id, current_weather
            )
        )

        forecast_weather_response_client = (
            await self.open_weather_client.get_forecast_weather_by_city(city=city)
        )
        if not forecast_weather_response_client:
            raise HTTPException(status_code=404, detail="Forecast Weather not found")

        city = forecast_weather_response_client.city.name
        latitude = forecast_weather_response_client.city.coord.lat
        longitude = forecast_weather_response_client.city.coord.lon
        list_forecast_wather = []
        for weather_data in forecast_weather_response_client.list:
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
                wind_speed=weather_data.wind.speed,
            )
            forecast_weather_response_repository = (
                await self.forecast_weather_repository.create(
                    db, authuser.id, forecast_weather
                )
            )
            list_forecast_wather.append(
                forecast_weather_response_repository.model_dump()
            )

        df = pd.DataFrame(list_forecast_wather)
        df["date_only"] = df["date"].dt.date
        daily_avg_temp = (
            df.groupby("date_only")["average_temperature"].mean().reset_index()
        )
        next_5_days = daily_avg_temp.head(5)

        gist_comment = CreateGistCommentRequest(
            city=city,
            latitude=latitude,
            longitude=longitude,
            current_temperature=float(
                current_weather_response_repository.current_temperature
            ),
            weather_description=str(
                current_weather_response_repository.weather_description
            ),
            forecast_day_1_date=str(next_5_days["date_only"].iloc[0]),
            forecast_day_1_temperature=next_5_days["average_temperature"].iloc[0],
            forecast_day_2_date=str(next_5_days["date_only"].iloc[1]),
            forecast_day_2_temperature=next_5_days["average_temperature"].iloc[1],
            forecast_day_3_date=str(next_5_days["date_only"].iloc[2]),
            forecast_day_3_temperature=next_5_days["average_temperature"].iloc[2],
            forecast_day_4_date=str(next_5_days["date_only"].iloc[3]),
            forecast_day_4_temperature=next_5_days["average_temperature"].iloc[3],
            forecast_day_5_date=str(next_5_days["date_only"].iloc[4]),
            forecast_day_5_temperature=next_5_days["average_temperature"].iloc[4],
        )

        gist_response = await self.github_client.create_gist_comment(
            comment=self.generate_comment(data=gist_comment)
        )

        gist_comment_response_repository = await self.gist_comment_repository.create(
            db, authuser.id, gist_response["comment_id"], gist_comment
        )

        return GistCommentResponse(**gist_comment_response_repository.model_dump())

    async def get_all_gist_comment_by_user(
        self, db: AsyncSession, user_id: int
    ) -> GetAllGistCommentResponse:
        comments = await self.gist_comment_repository.get_all_comments_by_user_id(
            db, user_id
        )
        if not comments:
            raise HTTPException(status_code=404, detail="Comments not found")

        comments_list = [
            GistCommentResponse(
                id=comment.id,
                comment_id=comment.comment_id,
                comment_date=comment.comment_date,
                city=comment.city,
                latitude=comment.latitude,
                longitude=comment.longitude,
                current_temperature=comment.current_temperature,
                weather_description=comment.weather_description,
                forecast_day_1_date=comment.forecast_day_1_date,
                forecast_day_1_temperature=comment.forecast_day_1_temperature,
                forecast_day_2_date=comment.forecast_day_2_date,
                forecast_day_2_temperature=comment.forecast_day_2_temperature,
                forecast_day_3_date=comment.forecast_day_3_date,
                forecast_day_3_temperature=comment.forecast_day_3_temperature,
                forecast_day_4_date=comment.forecast_day_4_date,
                forecast_day_4_temperature=comment.forecast_day_4_temperature,
                forecast_day_5_date=comment.forecast_day_5_date,
                forecast_day_5_temperature=comment.forecast_day_5_temperature,
            )
            for comment in comments
        ]
        return GetAllGistCommentResponse(comments=comments_list)

    async def update_gist_comment(
        self, db: AsyncSession, comment_id: int, data: PutGistCommentRequest
    ) -> PutGistCommentResponse:
        comment = await self.gist_comment_repository.get_gist_comment_by_id(
            db, comment_id
        )
        if not comment:
            raise HTTPException(status_code=404, detail="Comment not found")

        await self.github_client.edit_gist_comment(
            comment_id=comment_id,
            new_comment=self.generate_comment(
                CreateGistCommentRequest(
                    city=data.city,
                    latitude=data.latitude,
                    longitude=data.longitude,
                    current_temperature=data.current_temperature,
                    weather_description=data.weather_description,
                    forecast_day_1_date=data.forecast_day_1_date,
                    forecast_day_1_temperature=data.forecast_day_1_temperature,
                    forecast_day_2_date=data.forecast_day_2_date,
                    forecast_day_2_temperature=data.forecast_day_2_temperature,
                    forecast_day_3_date=data.forecast_day_3_date,
                    forecast_day_3_temperature=data.forecast_day_3_temperature,
                    forecast_day_4_date=data.forecast_day_4_date,
                    forecast_day_4_temperature=data.forecast_day_4_temperature,
                    forecast_day_5_date=data.forecast_day_5_date,
                    forecast_day_5_temperature=data.forecast_day_5_temperature,
                )
            ),
        )
        updated_comment = await self.gist_comment_repository.update(db, comment, data)

        return PutGistCommentResponse(
            message="Comment updated successfully",
            response=GistCommentResponse(
                id=updated_comment.id,
                comment_id=updated_comment.comment_id,
                comment_date=updated_comment.comment_date,
                city=updated_comment.city,
                latitude=updated_comment.latitude,
                longitude=updated_comment.longitude,
                current_temperature=updated_comment.current_temperature,
                weather_description=updated_comment.weather_description,
                forecast_day_1_date=updated_comment.forecast_day_1_date,
                forecast_day_1_temperature=updated_comment.forecast_day_1_temperature,
                forecast_day_2_date=updated_comment.forecast_day_2_date,
                forecast_day_2_temperature=updated_comment.forecast_day_2_temperature,
                forecast_day_3_date=updated_comment.forecast_day_3_date,
                forecast_day_3_temperature=updated_comment.forecast_day_3_temperature,
                forecast_day_4_date=updated_comment.forecast_day_4_date,
                forecast_day_4_temperature=updated_comment.forecast_day_4_temperature,
                forecast_day_5_date=updated_comment.forecast_day_5_date,
                forecast_day_5_temperature=updated_comment.forecast_day_5_temperature,
            ),
        )

    async def delete_gist_comment(
        self, db: AsyncSession, comment_id: int
    ) -> DeleteGistCommentResponse:
        comment = await self.gist_comment_repository.get_gist_comment_by_id(
            db, comment_id
        )
        if not comment:
            raise HTTPException(status_code=404, detail="Comment not found")

        await self.github_client.delete_gist_comment(comment_id=comment_id)
        await self.gist_comment_repository.delete(db, comment.comment_id)
        return DeleteGistCommentResponse(
            message="Comment deleted successfully",
            response=GistCommentResponse(
                id=comment.id,
                comment_id=comment.comment_id,
                comment_date=comment.comment_date,
                city=comment.city,
                latitude=comment.latitude,
                longitude=comment.longitude,
                current_temperature=comment.current_temperature,
                weather_description=comment.weather_description,
                forecast_day_1_date=comment.forecast_day_1_date,
                forecast_day_1_temperature=comment.forecast_day_1_temperature,
                forecast_day_2_date=comment.forecast_day_2_date,
                forecast_day_2_temperature=comment.forecast_day_2_temperature,
                forecast_day_3_date=comment.forecast_day_3_date,
                forecast_day_3_temperature=comment.forecast_day_3_temperature,
                forecast_day_4_date=comment.forecast_day_4_date,
                forecast_day_4_temperature=comment.forecast_day_4_temperature,
                forecast_day_5_date=comment.forecast_day_5_date,
                forecast_day_5_temperature=comment.forecast_day_5_temperature,
            ),
        )
