from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.gist_comments.gist_comment_schemas import (
    CreateGistCommentRequest,
    GistCommentResponse,
    PutGistCommentRequest,
)
from app.database.models.gist_comment import GistComment


class GistCommentRepository:
    async def create(
        self,
        db: AsyncSession,
        user_id: int,
        comment_id: int,
        gist_comment: CreateGistCommentRequest,
    ) -> GistCommentResponse:
        gist_comment_instance = GistComment(
            comment_id=comment_id,
            city=gist_comment.city,
            latitude=gist_comment.latitude,
            longitude=gist_comment.longitude,
            current_temperature=gist_comment.current_temperature,
            weather_description=gist_comment.weather_description,
            forecast_day_1_date=str(gist_comment.forecast_day_1_date),
            forecast_day_1_temperature=gist_comment.forecast_day_1_temperature,
            forecast_day_2_date=str(gist_comment.forecast_day_2_date),
            forecast_day_2_temperature=gist_comment.forecast_day_2_temperature,
            forecast_day_3_date=str(gist_comment.forecast_day_3_date),
            forecast_day_3_temperature=gist_comment.forecast_day_3_temperature,
            forecast_day_4_date=str(gist_comment.forecast_day_4_date),
            forecast_day_4_temperature=gist_comment.forecast_day_4_temperature,
            forecast_day_5_date=str(gist_comment.forecast_day_5_date),
            forecast_day_5_temperature=gist_comment.forecast_day_5_temperature,
            user_id=user_id,
        )

        db.add(gist_comment_instance)
        db.commit()
        db.refresh(gist_comment_instance)

        return GistCommentResponse(
            id=gist_comment_instance.id,
            comment_id=gist_comment_instance.comment_id,
            city=gist_comment_instance.city,
            latitude=gist_comment_instance.latitude,
            longitude=gist_comment_instance.longitude,
            comment_date=gist_comment_instance.comment_date,
            current_temperature=gist_comment_instance.current_temperature,
            weather_description=gist_comment_instance.weather_description,
            forecast_day_1_date=gist_comment_instance.forecast_day_1_date,
            forecast_day_1_temperature=gist_comment_instance.forecast_day_1_temperature,
            forecast_day_2_date=gist_comment_instance.forecast_day_2_date,
            forecast_day_2_temperature=gist_comment_instance.forecast_day_2_temperature,
            forecast_day_3_date=gist_comment_instance.forecast_day_3_date,
            forecast_day_3_temperature=gist_comment_instance.forecast_day_3_temperature,
            forecast_day_4_date=gist_comment_instance.forecast_day_4_date,
            forecast_day_4_temperature=gist_comment_instance.forecast_day_4_temperature,
            forecast_day_5_date=gist_comment_instance.forecast_day_5_date,
            forecast_day_5_temperature=gist_comment_instance.forecast_day_5_temperature,
            user_id=gist_comment_instance.user_id,
        )

    async def get_all_comments_by_user_id(self, db: AsyncSession, user_id: int):
        return db.query(GistComment).filter(GistComment.user_id == user_id).all()

    async def get_gist_comment_by_id(self, db: AsyncSession, comment_id: int):
        return (
            db.query(GistComment).filter(GistComment.comment_id == comment_id).first()
        )

    async def update(
        self, db: AsyncSession, gist_comment: GistComment, data: PutGistCommentRequest
    ):
        gist_comment.city = data.city if data.city else gist_comment.city
        gist_comment.latitude = (
            data.latitude if data.latitude else gist_comment.latitude
        )
        gist_comment.longitude = (
            data.longitude if data.longitude else gist_comment.longitude
        )
        gist_comment.current_temperature = (
            data.current_temperature
            if data.current_temperature
            else gist_comment.current_temperature
        )
        gist_comment.weather_description = (
            data.weather_description
            if data.weather_description
            else gist_comment.weather_description
        )
        gist_comment.forecast_day_1_date = (
            data.forecast_day_1_date
            if data.forecast_day_1_date
            else gist_comment.forecast_day_1_date
        )
        gist_comment.forecast_day_1_temperature = (
            data.forecast_day_1_temperature
            if data.forecast_day_1_temperature
            else gist_comment.forecast_day_1_temperature
        )
        gist_comment.forecast_day_2_date = (
            data.forecast_day_2_date
            if data.forecast_day_2_date
            else gist_comment.forecast_day_2_date
        )
        gist_comment.forecast_day_2_temperature = (
            data.forecast_day_2_temperature
            if data.forecast_day_2_temperature
            else gist_comment.forecast_day_2_temperature
        )
        gist_comment.forecast_day_3_date = (
            data.forecast_day_3_date
            if data.forecast_day_3_date
            else gist_comment.forecast_day_3_date
        )
        gist_comment.forecast_day_3_temperature = (
            data.forecast_day_3_temperature
            if data.forecast_day_3_temperature
            else gist_comment.forecast_day_3_temperature
        )
        gist_comment.forecast_day_4_date = (
            data.forecast_day_4_date
            if data.forecast_day_4_date
            else gist_comment.forecast_day_4_date
        )
        gist_comment.forecast_day_4_temperature = (
            data.forecast_day_4_temperature
            if data.forecast_day_4_temperature
            else gist_comment.forecast_day_4_temperature
        )
        gist_comment.forecast_day_5_date = (
            data.forecast_day_5_date
            if data.forecast_day_5_date
            else gist_comment.forecast_day_5_date
        )
        gist_comment.forecast_day_5_temperature = (
            data.forecast_day_5_temperature
            if data.forecast_day_5_temperature
            else gist_comment.forecast_day_5_temperature
        )
        db.commit()
        db.refresh(gist_comment)
        return gist_comment

    async def delete(self, db: AsyncSession, comment_id: int):
        comment_entry = (
            db.query(GistComment).filter(GistComment.comment_id == comment_id).first()
        )
        if comment_entry:
            db.delete(comment_entry)
            db.commit()
