from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database.base import Base


class GistComment(Base):
    __tablename__ = "gist_comments"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, nullable=False)
    comment_date = Column(DateTime, default=datetime.now(), nullable=False)
    current_temperature = Column(Float, nullable=False)
    weather_description = Column(String, nullable=False)
    forecast_day_1_date = Column(String, nullable=False)
    forecast_day_1_temperature = Column(Float, nullable=False)
    forecast_day_2_date = Column(String, nullable=False)
    forecast_day_2_temperature = Column(Float, nullable=False)
    forecast_day_3_date = Column(String, nullable=False)
    forecast_day_3_temperature = Column(Float, nullable=False)
    forecast_day_4_date = Column(String, nullable=False)
    forecast_day_4_temperature = Column(Float, nullable=False)
    forecast_day_5_date = Column(String, nullable=False)
    forecast_day_5_temperature = Column(Float, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="gist_comments")
