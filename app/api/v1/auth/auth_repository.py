import random
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.auth.auth_schemas import PostSignUpRequest
from app.core.security import decode_access_token
from app.database.models.blacklist import TokenBlacklist
from app.database.models.user import User


class AuthRepository:
    async def create_user(self, db: AsyncSession, data: PostSignUpRequest):
        db_user = User(
            username=data.username,
            password=data.password,
            name=data.name,
            email=data.email,
            cpf=data.cpf,
            cnpj=data.cnpj,
            is_active=True,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    async def get_user_by_id(self, db: AsyncSession, id: int):
        return db.query(User).filter(User.id == id).first()

    async def get_user_by_email(self, db: AsyncSession, email: str):
        return db.query(User).filter(User.email == email).first()

    async def update_password(self, db: AsyncSession, email: str, new_password: str):
        user = db.query(User).filter(User.email == email).first()
        if user:
            user.password = new_password  # type: ignore
            db.commit()

    def verify_token(self, token: str):
        payload = decode_access_token(token)
        return payload if payload else None

    async def add_token(self, db: AsyncSession, token_id: str):
        token = TokenBlacklist(id=token_id)
        db.add(token)
        db.commit()
        db.refresh(token)
        return token

    async def is_token_blacklisted(self, db: AsyncSession, token_id: str) -> bool:
        return (
            db.query(TokenBlacklist).filter(TokenBlacklist.id == token_id).first()
            is not None
        )

    def generate_pin(self):
        return "".join([str(random.randint(0, 9)) for _ in range(6)])

    async def save_pin(
        self, db: AsyncSession, user_id: int, pin: str, expiration: datetime
    ):
        user = db.query(User).filter(User.id == user_id).first()
        user.reset_pin = pin  # type: ignore
        user.reset_pin_expiration = expiration  # type: ignore
        db.add(user)
        db.commit()

    async def verify_pin(self, db: AsyncSession, email: str, pin: str):
        user = db.query(User).filter(User.email == email).first()

        if user:
            if user.reset_pin == pin:
                if user.reset_pin_expiration >= datetime.now():
                    return {
                        "email": user.email,
                        "expiration": user.reset_pin_expiration,
                    }
                return {"error": "PIN has expired"}
            return {"error": "Invalid PIN"}

        return {"error": "User not found"}
