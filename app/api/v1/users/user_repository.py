from sqlalchemy.orm import Session

from app.api.v1.users.user_schemas import PutUserRequest, PutUsersMeRequest
from app.database.models.user import User


class UserRepository:
    async def get_user_by_id(self, db: Session, user_id: int):
        return db.query(User).filter(User.id == user_id).first()

    async def get_user_by_email(self, db: Session, email: str):
        return db.query(User).filter(User.email == email).first()

    async def update_user_profile(
        self, db: Session, user: User, data: PutUsersMeRequest
    ):
        user.name = data.name if data.name else user.name  # type: ignore
        user.email = data.email if data.email else user.email  # type: ignore
        db.commit()
        db.refresh(user)
        return user

    async def update_user(self, db: Session, user: User, data: PutUserRequest):
        user.name = data.name if data.name else user.name  # type: ignore
        user.email = data.email if data.email else user.email  # type: ignore
        db.commit()
        db.refresh(user)
        return user
    
    async def delete_user(self, db: Session, user_id: int):
        user_entry = (
            db.query(User).filter(User.id == user_id).first()
        )
        if user_entry:
            db.delete(user_entry)
            db.commit()
            return user_entry

    async def get_all_users(self, db: Session):
        return db.query(User).all()