from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String

from app.database.base import Base


class CurrentWeather(Base):
    __tablename__ = 'current_weather'

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, index=True, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    current_temperature = Column(Float, nullable=False)
    feels_like = Column(Float, nullable=False)
    temp_min = Column(Float, nullable=False)
    temp_max = Column(Float, nullable=False)
    pressure = Column(Integer, nullable=False)
    humidity = Column(Integer, nullable=False)
    visibility = Column(Integer, nullable=True)
    wind_speed = Column(Float, nullable=False)
    wind_deg = Column(Integer, nullable=False)
    wind_gust = Column(Float, nullable=True)
    cloudiness = Column(Integer, nullable=False)
    weather_description = Column(String, nullable=False)
    observation_datetime = Column(DateTime, default=datetime.now(), nullable=False)
    sunrise = Column(DateTime, nullable=False)
    sunset = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    user = relationship("User", back_populates="current_weather")

