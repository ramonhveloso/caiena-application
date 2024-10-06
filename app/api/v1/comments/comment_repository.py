from sqlalchemy.orm import Session

from app.api.v1.comments.comment_schemas import CreateCommentRequest, CreateCommentResponse, PutWeatherCurrentRequest
from app.database.models.comment import Comment


from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

class CommentRepository:
    async def create(self, db: AsyncSession, user_id: int, comment: CreateCommentRequest) -> CreateCommentResponse:
        """
        Cria e salva um registro de clima atual no banco de dados.
        
        Args:
            db (AsyncSession): Sessão ativa do banco de dados.
            user_id (str): ID do usuário para associar o clima.
            comment (CreateCommentRequest): Objeto contendo os dados do clima a serem salvos.
        
        Returns:
            CreateCommentResponse: Instância do modelo contendo os dados salvos.
        """
        # Criar uma instância do modelo Comment com os dados fornecidos
        comment_instance = Comment(
            city=comment.name,
            latitude=comment.coord.lat,
            longitude=comment.coord.lon,
            current_temperature=comment.main.temp,
            feels_like=comment.main.feels_like,
            temp_min=comment.main.temp_min,
            temp_max=comment.main.temp_max,
            pressure=comment.main.pressure,
            humidity=comment.main.humidity,
            visibility=comment.visibility,
            wind_speed=comment.wind.speed,
            wind_deg=comment.wind.deg,
            wind_gust=comment.wind.gust,
            cloudiness=comment.clouds.all,
            weather_description=comment.weather[0].description,
            observation_datetime=datetime.fromtimestamp(comment.dt),  # Conversão de Unix timestamp para datetime
            sunrise=datetime.fromtimestamp(comment.sys.sunrise),  # Conversão de Unix timestamp para datetime
            sunset=datetime.fromtimestamp(comment.sys.sunset),  # Conversão de Unix timestamp para datetime
            user_id=user_id  # Relaciona o registro ao usuário
        )
        
        # Adiciona o objeto à sessão do banco de dados e confirma a transação
        db.add(comment_instance)
        db.commit()
        db.refresh(comment_instance)

        # Retornar uma instância de CreateCommentResponse com os dados salvos
        return CreateCommentResponse(
            id=comment_instance.id,
            city=comment_instance.city,
            latitude=comment_instance.latitude,
            longitude=comment_instance.longitude,
            current_temperature=comment_instance.current_temperature,
            feels_like=comment_instance.feels_like,
            temp_min=comment_instance.temp_min,
            temp_max=comment_instance.temp_max,
            pressure=comment_instance.pressure,
            humidity=comment_instance.humidity,
            visibility=comment_instance.visibility,
            wind_speed=comment_instance.wind_speed,
            wind_deg=comment_instance.wind_deg,
            wind_gust=comment_instance.wind_gust,
            cloudiness=comment_instance.cloudiness,
            weather_description=comment_instance.weather_description,
            observation_datetime=comment_instance.observation_datetime,
            sunrise=comment_instance.sunrise,
            sunset=comment_instance.sunset,
            user_id=comment_instance.user_id
        )

    async def get_by_city(self, db: Session, city: str) -> list[Comment]:
        """
        Retorna uma lista de registros de clima atual para uma cidade específica.
        
        Args:
            db (Session): Sessão ativa do banco de dados.
            city (str): Nome da cidade para buscar os registros de clima.
        
        Returns:
            list[Comment]: Lista de objetos Comment com os dados encontrados.
        """
        return db.query(Comment).filter(Comment.city == city).all()

    async def get_all_weathers_by_user_id(self, db: Session, user_id: int):
        """
        Busca todos os registros de clima atual pelo ID do usuario.
        
        Args:
            db (Session): Sessão ativa do banco de dados.
            user_id (int): ID do usuario.
        
        Returns:
            Comment: Instância do modelo Comment correspondente ao ID fornecido.
        """
        return db.query(Comment).filter(Comment.user_id == user_id).all()
    
    async def get_comment_by_id(self, db: Session, weather_id: int):
        """
        Busca um registro específico de clima atual pelo ID.
        
        Args:
            db (Session): Sessão ativa do banco de dados.
            weather_id (int): ID do registro de clima.

        Returns:
            Comment: Instância do modelo Comment correspondente ao ID fornecido.
        """
        return db.query(Comment).filter(Comment.id == weather_id).first()
    
    async def update(self, db: Session, comment: Comment, data: PutWeatherCurrentRequest):
        """Atualiza os dados de um clima específico."""
        comment.city = data.city if data.city else comment.city # type: ignore
        comment.latitude = data.latitude if data.latitude else comment.latitude
        comment.longitude = data.longitude if data.longitude else comment.longitude
        comment.current_temperature = data.current_temperature if data.current_temperature else comment.current_temperature
        comment.feels_like = data.feels_like if data.feels_like else comment.feels_like
        comment.temp_min = data.temp_min if data.temp_min else comment.temp_min
        comment.temp_max = data.temp_max if data.temp_max else comment.temp_max
        comment.pressure = data.pressure if data.pressure else comment.pressure
        comment.humidity = data.humidity if data.humidity else comment.humidity
        comment.visibility = data.visibility if data.visibility else comment.visibility
        comment.wind_speed = data.wind_speed if data.wind_speed else comment.wind_speed
        comment.wind_deg = data.wind_deg if data.wind_deg else comment.wind_deg
        comment.wind_gust = data.wind_gust if data.wind_gust else comment.wind_gust
        comment.cloudiness = data.cloudiness if data.cloudiness else comment.cloudiness
        comment.weather_description = data.weather_description if data.weather_description else comment.weather_description
        comment.observation_datetime = data.observation_datetime if data.observation_datetime else comment.observation_datetime
        comment.sunrise = data.sunrise if data.sunrise else comment.sunrise
        comment.sunset = data.sunset if data.sunset else comment.sunset
        comment.user_id = data.user_id if data.user_id else comment.user_id
        db.commit()
        db.refresh(comment)
        return comment

    async def delete(self, db: Session, weather_id: int):
        """
        Exclui um registro de clima atual do banco de dados pelo ID.
        
        Args:
            db (Session): Sessão ativa do banco de dados.
            weather_id (int): ID do registro de clima a ser excluído.
        
        Returns:
            None
        """
        weather_entry = db.query(Comment).filter(Comment.id == weather_id).first()
        if weather_entry:
            db.delete(weather_entry)
            db.commit()
