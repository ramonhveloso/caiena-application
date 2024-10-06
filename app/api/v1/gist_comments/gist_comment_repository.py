from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.gist_comments.gist_comment_schemas import (
    CreateGistCommentRequest,
    GistCommentResponse,
)
from app.database.models.gist_comment import GistComment


class GistCommentRepository:
    async def create(
        self, db: AsyncSession, user_id: int, gist_comment: CreateGistCommentRequest
    ) -> GistCommentResponse:
        gist_comment_instance = GistComment(
            city=gist_comment.name,
            latitude=gist_comment.coord.lat,
            longitude=gist_comment.coord.lon,
            current_temperature=gist_comment.main.temp,
            feels_like=gist_comment.main.feels_like,
            temp_min=gist_comment.main.temp_min,
            temp_max=gist_comment.main.temp_max,
            pressure=gist_comment.main.pressure,
            humidity=gist_comment.main.humidity,
            visibility=gist_comment.visibility,
            wind_speed=gist_comment.wind.speed,
            wind_deg=gist_comment.wind.deg,
            wind_gust=gist_comment.wind.gust,
            cloudiness=gist_comment.clouds.all,
            weather_description=gist_comment.weather[0].description,
            observation_datetime=datetime.fromtimestamp(gist_comment.dt),
            sunrise=datetime.fromtimestamp(gist_comment.sys.sunrise),
            sunset=datetime.fromtimestamp(gist_comment.sys.sunset),
            user_id=user_id,
        )

        db.add(gist_comment_instance)
        db.commit()
        db.refresh(gist_comment_instance)

        return GistCommentResponse(
            id=gist_comment_instance.id,
            city=gist_comment_instance.city,
            latitude=gist_comment_instance.latitude,
            longitude=gist_comment_instance.longitude,
            current_temperature=gist_comment_instance.current_temperature,
            feels_like=gist_comment_instance.feels_like,
            temp_min=gist_comment_instance.temp_min,
            temp_max=gist_comment_instance.temp_max,
            pressure=gist_comment_instance.pressure,
            humidity=gist_comment_instance.humidity,
            visibility=gist_comment_instance.visibility,
            wind_speed=gist_comment_instance.wind_speed,
            wind_deg=gist_comment_instance.wind_deg,
            wind_gust=gist_comment_instance.wind_gust,
            cloudiness=gist_comment_instance.cloudiness,
            weather_description=gist_comment_instance.weather_description,
            observation_datetime=gist_comment_instance.observation_datetime,
            sunrise=gist_comment_instance.sunrise,
            sunset=gist_comment_instance.sunset,
            user_id=gist_comment_instance.user_id,
        )

    # async def get_by_city(self, db: AsyncSession, city: str) -> list[GistComment]:
    #     return db.query(GistComment).filter(GistComment.city == city).all()

    # async def get_all_weathers_by_user_id(self, db: AsyncSession, user_id: int):
    #     return db.query(GistComment).filter(GistComment.user_id == user_id).all()

    # async def get_gist_comment_by_id(self, db: AsyncSession, weather_id: int):
    #     return db.query(GistComment).filter(GistComment.id == weather_id).first()

    # async def update(self, db: AsyncSession, gist_comment: GistComment, data: PutWeatherCurrentRequest):
    #     gist_comment.city = data.city if data.city else gist_comment.city # type: ignore
    #     gist_comment.latitude = data.latitude if data.latitude else gist_comment.latitude
    #     gist_comment.longitude = data.longitude if data.longitude else gist_comment.longitude
    #     gist_comment.current_temperature = data.current_temperature if data.current_temperature else gist_comment.current_temperature
    #     gist_comment.feels_like = data.feels_like if data.feels_like else gist_comment.feels_like
    #     gist_comment.temp_min = data.temp_min if data.temp_min else gist_comment.temp_min
    #     gist_comment.temp_max = data.temp_max if data.temp_max else gist_comment.temp_max
    #     gist_comment.pressure = data.pressure if data.pressure else gist_comment.pressure
    #     gist_comment.humidity = data.humidity if data.humidity else gist_comment.humidity
    #     gist_comment.visibility = data.visibility if data.visibility else gist_comment.visibility
    #     gist_comment.wind_speed = data.wind_speed if data.wind_speed else gist_comment.wind_speed
    #     gist_comment.wind_deg = data.wind_deg if data.wind_deg else gist_comment.wind_deg
    #     gist_comment.wind_gust = data.wind_gust if data.wind_gust else gist_comment.wind_gust
    #     gist_comment.cloudiness = data.cloudiness if data.cloudiness else gist_comment.cloudiness
    #     gist_comment.weather_description = data.weather_description if data.weather_description else gist_comment.weather_description
    #     gist_comment.observation_datetime = data.observation_datetime if data.observation_datetime else gist_comment.observation_datetime
    #     gist_comment.sunrise = data.sunrise if data.sunrise else gist_comment.sunrise
    #     gist_comment.sunset = data.sunset if data.sunset else gist_comment.sunset
    #     gist_comment.user_id = data.user_id if data.user_id else gist_comment.user_id
    #     db.commit()
    #     db.refresh(gist_comment)
    #     return gist_comment

    # async def delete(self, db: AsyncSession, weather_id: int):
    #     weather_entry = db.query(GistComment).filter(GistComment.id == weather_id).first()
    #     if weather_entry:
    #         db.delete(weather_entry)
    #         db.commit()
