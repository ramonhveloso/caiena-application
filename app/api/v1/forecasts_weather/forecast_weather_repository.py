from sqlalchemy.orm import Session

from app.api.v1.forecasts_weather.forecast_weather_schemas import CreateForecastWeatherRequest, CreateForecastWeatherResponse, PutWeatherForecastRequest

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.forecast_weather import ForecastWeather

class ForecastWeatherRepository:
    async def create(self, db: AsyncSession, user_id: int, forecast_weather: CreateForecastWeatherRequest) -> CreateForecastWeatherResponse:
        """
        Cria e salva um registro de clima atual no banco de dados.
        
        Args:
            db (AsyncSession): Sessão ativa do banco de dados.
            user_id (str): ID do usuário para associar o clima.
            forecast_weather (CreateForecastWeatherRequest): Objeto contendo os dados do clima a serem salvos.
        
        Returns:
            CreateForecastWeatherResponse: Instância do modelo contendo os dados salvos.
        """
        # Criar uma instância do modelo ForecastWeather com os dados fornecidos
        forecast_weather_instance = ForecastWeather(
            city=forecast_weather.city,
            latitude=forecast_weather.latitude,
            longitude=forecast_weather.longitude,
            date=forecast_weather.date,
            average_temperature=forecast_weather.average_temperature,
            min_temperature=forecast_weather.min_temperature,
            max_temperature=forecast_weather.max_temperature,
            weather_description=forecast_weather.weather_description,
            humidity=forecast_weather.humidity,
            wind_speed=forecast_weather.wind_speed,
            user_id=user_id 
        )
        
        # Adiciona o objeto à sessão do banco de dados e confirma a transação
        db.add(forecast_weather_instance)
        db.commit()
        db.refresh(forecast_weather_instance)

        # Retornar uma instância de CreateForecastWeatherResponse com os dados salvos
        return CreateForecastWeatherResponse(
            id=forecast_weather_instance.id,
            city=forecast_weather_instance.city,
            latitude=forecast_weather_instance.latitude,
            longitude=forecast_weather_instance.longitude,
            date=forecast_weather_instance.date,
            average_temperature=forecast_weather_instance.average_temperature,
            min_temperature=forecast_weather_instance.min_temperature,
            max_temperature=forecast_weather_instance.max_temperature,
            weather_description=forecast_weather_instance.weather_description,
            humidity=forecast_weather_instance.humidity,
            wind_speed=forecast_weather_instance.wind_speed,
            user_id=forecast_weather_instance.user_id 
        )

    async def get_by_city(self, db: Session, city: str) -> list[ForecastWeather]:
        """
        Retorna uma lista de registros de clima atual para uma cidade específica.
        
        Args:
            db (Session): Sessão ativa do banco de dados.
            city (str): Nome da cidade para buscar os registros de clima.
        
        Returns:
            list[ForecastWeather]: Lista de objetos ForecastWeather com os dados encontrados.
        """
        return db.query(ForecastWeather).filter(ForecastWeather.city == city).all()

    async def get_all_weathers_by_user_id(self, db: Session, user_id: int):
        """
        Busca todos os registros de clima atual pelo ID do usuario.
        
        Args:
            db (Session): Sessão ativa do banco de dados.
            user_id (int): ID do usuario.
        
        Returns:
            ForecastWeather: Instância do modelo ForecastWeather correspondente ao ID fornecido.
        """
        return db.query(ForecastWeather).filter(ForecastWeather.user_id == user_id).all()
    
    async def get_forecast_weather_by_id(self, db: Session, weather_id: int):
        """
        Busca um registro específico de clima atual pelo ID.
        
        Args:
            db (Session): Sessão ativa do banco de dados.
            weather_id (int): ID do registro de clima.

        Returns:
            ForecastWeather: Instância do modelo ForecastWeather correspondente ao ID fornecido.
        """
        return db.query(ForecastWeather).filter(ForecastWeather.id == weather_id).first()
    
    async def update(self, db: Session, forecast_weather: ForecastWeather, data: PutWeatherForecastRequest):
        """Atualiza os dados de um clima específico."""
        forecast_weather.city = data.city if data.city else forecast_weather.city # type: ignore
        forecast_weather.latitude = data.latitude if data.latitude else forecast_weather.latitude # type: ignore
        forecast_weather.longitude = data.longitude if data.longitude else forecast_weather.longitude # type: ignore
        forecast_weather.date = data.date if data.date else forecast_weather.date # type: ignore
        forecast_weather.average_temperature = data.average_temperature if data.average_temperature else forecast_weather.average_temperature # type: ignore
        forecast_weather.min_temperature = data.min_temperature if data.min_temperature else forecast_weather.min_temperature # type: ignore
        forecast_weather.max_temperature = data.max_temperature if data.max_temperature else forecast_weather.max_temperature # type: ignore
        forecast_weather.humidity = data.humidity if data.humidity else forecast_weather.humidity # type: ignore
        forecast_weather.wind_speed = data.wind_speed if data.wind_speed else forecast_weather.wind_speed # type: ignore
        forecast_weather.weather_description = data.weather_description if data.weather_description else forecast_weather.weather_description # type: ignore
        forecast_weather.user_id = data.user_id if data.user_id else forecast_weather.user_id # type: ignore
        db.commit()
        db.refresh(forecast_weather)
        return forecast_weather

    async def delete(self, db: Session, weather_id: int):
        """
        Exclui um registro de clima atual do banco de dados pelo ID.
        
        Args:
            db (Session): Sessão ativa do banco de dados.
            weather_id (int): ID do registro de clima a ser excluído.
        
        Returns:
            None
        """
        weather_entry = db.query(ForecastWeather).filter(ForecastWeather.id == weather_id).first()
        if weather_entry:
            db.delete(weather_entry)
            db.commit()
