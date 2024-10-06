from sqlalchemy.orm import Session

from app.api.v1.current_weather.current_weather_schemas import CreateCurrentWeatherRequest, CreateCurrentWeatherResponse, PutWeatherCurrentRequest
from app.database.models.current_weather import CurrentWeather


from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

class CurrentWeatherRepository:
    async def create(self, db: AsyncSession, user_id: int, current_weather: CreateCurrentWeatherRequest) -> CreateCurrentWeatherResponse:
        """
        Cria e salva um registro de clima atual no banco de dados.
        
        Args:
            db (AsyncSession): Sessão ativa do banco de dados.
            user_id (str): ID do usuário para associar o clima.
            current_weather (CreateCurrentWeatherRequest): Objeto contendo os dados do clima a serem salvos.
        
        Returns:
            CreateCurrentWeatherResponse: Instância do modelo contendo os dados salvos.
        """
        # Criar uma instância do modelo CurrentWeather com os dados fornecidos
        current_weather_instance = CurrentWeather(
            city=current_weather.name,
            latitude=current_weather.coord.lat,
            longitude=current_weather.coord.lon,
            current_temperature=current_weather.main.temp,
            feels_like=current_weather.main.feels_like,
            temp_min=current_weather.main.temp_min,
            temp_max=current_weather.main.temp_max,
            pressure=current_weather.main.pressure,
            humidity=current_weather.main.humidity,
            visibility=current_weather.visibility,
            wind_speed=current_weather.wind.speed,
            wind_deg=current_weather.wind.deg,
            wind_gust=current_weather.wind.gust,
            cloudiness=current_weather.clouds.all,
            weather_description=current_weather.weather[0].description,
            observation_datetime=datetime.fromtimestamp(current_weather.dt),  # Conversão de Unix timestamp para datetime
            sunrise=datetime.fromtimestamp(current_weather.sys.sunrise),  # Conversão de Unix timestamp para datetime
            sunset=datetime.fromtimestamp(current_weather.sys.sunset),  # Conversão de Unix timestamp para datetime
            user_id=user_id  # Relaciona o registro ao usuário
        )
        
        # Adiciona o objeto à sessão do banco de dados e confirma a transação
        db.add(current_weather_instance)
        db.commit()
        db.refresh(current_weather_instance)

        # Retornar uma instância de CreateCurrentWeatherResponse com os dados salvos
        return CreateCurrentWeatherResponse(
            id=current_weather_instance.id,
            city=current_weather_instance.city,
            latitude=current_weather_instance.latitude,
            longitude=current_weather_instance.longitude,
            current_temperature=current_weather_instance.current_temperature,
            feels_like=current_weather_instance.feels_like,
            temp_min=current_weather_instance.temp_min,
            temp_max=current_weather_instance.temp_max,
            pressure=current_weather_instance.pressure,
            humidity=current_weather_instance.humidity,
            visibility=current_weather_instance.visibility,
            wind_speed=current_weather_instance.wind_speed,
            wind_deg=current_weather_instance.wind_deg,
            wind_gust=current_weather_instance.wind_gust,
            cloudiness=current_weather_instance.cloudiness,
            weather_description=current_weather_instance.weather_description,
            observation_datetime=current_weather_instance.observation_datetime,
            sunrise=current_weather_instance.sunrise,
            sunset=current_weather_instance.sunset,
            user_id=current_weather_instance.user_id
        )

    async def get_by_city(self, db: Session, city: str) -> list[CurrentWeather]:
        """
        Retorna uma lista de registros de clima atual para uma cidade específica.
        
        Args:
            db (Session): Sessão ativa do banco de dados.
            city (str): Nome da cidade para buscar os registros de clima.
        
        Returns:
            list[CurrentWeather]: Lista de objetos CurrentWeather com os dados encontrados.
        """
        return db.query(CurrentWeather).filter(CurrentWeather.city == city).all()

    async def get_all_weathers_by_user_id(self, db: Session, user_id: int):
        """
        Busca todos os registros de clima atual pelo ID do usuario.
        
        Args:
            db (Session): Sessão ativa do banco de dados.
            user_id (int): ID do usuario.
        
        Returns:
            CurrentWeather: Instância do modelo CurrentWeather correspondente ao ID fornecido.
        """
        return db.query(CurrentWeather).filter(CurrentWeather.user_id == user_id).all()
    
    async def get_current_weather_by_id(self, db: Session, weather_id: int):
        """
        Busca um registro específico de clima atual pelo ID.
        
        Args:
            db (Session): Sessão ativa do banco de dados.
            weather_id (int): ID do registro de clima.

        Returns:
            CurrentWeather: Instância do modelo CurrentWeather correspondente ao ID fornecido.
        """
        return db.query(CurrentWeather).filter(CurrentWeather.id == weather_id).first()
    
    async def update(self, db: Session, current_weather: CurrentWeather, data: PutWeatherCurrentRequest):
        """Atualiza os dados de um clima específico."""
        current_weather.city = data.city if data.city else current_weather.city # type: ignore
        current_weather.latitude = data.latitude if data.latitude else current_weather.latitude
        current_weather.longitude = data.longitude if data.longitude else current_weather.longitude
        current_weather.current_temperature = data.current_temperature if data.current_temperature else current_weather.current_temperature
        current_weather.feels_like = data.feels_like if data.feels_like else current_weather.feels_like
        current_weather.temp_min = data.temp_min if data.temp_min else current_weather.temp_min
        current_weather.temp_max = data.temp_max if data.temp_max else current_weather.temp_max
        current_weather.pressure = data.pressure if data.pressure else current_weather.pressure
        current_weather.humidity = data.humidity if data.humidity else current_weather.humidity
        current_weather.visibility = data.visibility if data.visibility else current_weather.visibility
        current_weather.wind_speed = data.wind_speed if data.wind_speed else current_weather.wind_speed
        current_weather.wind_deg = data.wind_deg if data.wind_deg else current_weather.wind_deg
        current_weather.wind_gust = data.wind_gust if data.wind_gust else current_weather.wind_gust
        current_weather.cloudiness = data.cloudiness if data.cloudiness else current_weather.cloudiness
        current_weather.weather_description = data.weather_description if data.weather_description else current_weather.weather_description
        current_weather.observation_datetime = data.observation_datetime if data.observation_datetime else current_weather.observation_datetime
        current_weather.sunrise = data.sunrise if data.sunrise else current_weather.sunrise
        current_weather.sunset = data.sunset if data.sunset else current_weather.sunset
        current_weather.user_id = data.user_id if data.user_id else current_weather.user_id
        db.commit()
        db.refresh(current_weather)
        return current_weather

    async def delete(self, db: Session, weather_id: int):
        """
        Exclui um registro de clima atual do banco de dados pelo ID.
        
        Args:
            db (Session): Sessão ativa do banco de dados.
            weather_id (int): ID do registro de clima a ser excluído.
        
        Returns:
            None
        """
        weather_entry = db.query(CurrentWeather).filter(CurrentWeather.id == weather_id).first()
        if weather_entry:
            db.delete(weather_entry)
            db.commit()
