from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from app.database.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    name = Column(String, unique=False, index=True)
    email = Column(String, unique=True, index=True)
    cpf = Column(String, unique=True, index=True)
    cnpj = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    reset_pin = Column(String, nullable=True)
    reset_pin_expiration = Column(DateTime, nullable=True)

    # Relacionamento com a tabela CurrentWeather e ForecastWeather
    current_weather = relationship("CurrentWeather", back_populates="user")
    forecast_weather = relationship("ForecastWeather", back_populates="user")
    gist_comments= relationship("GistComment", back_populates="user")