from sqlalchemy.orm import relationship
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String

from app.database.base import Base


class ForecastWeather(Base):
    __tablename__ = 'forecast_weather'

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, index=True, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    date = Column(DateTime, nullable=False)
    average_temperature = Column(Float, nullable=False)
    min_temperature = Column(Float, nullable=False)
    max_temperature = Column(Float, nullable=False)
    weather_description = Column(String, nullable=False) 
    humidity = Column(Float, nullable=True)
    wind_speed = Column(Float, nullable=True)  
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    user = relationship("User", back_populates="forecast_weather")