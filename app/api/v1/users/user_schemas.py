from typing import List, Optional

from pydantic import BaseModel, EmailStr


class GetUsersMeResponse(BaseModel):
    id: int
    email: EmailStr
    name: str

    class Config:
        from_attributes = True

    @classmethod
    def model_validate(cls, data):
        if isinstance(data, cls):
            data = data.model_dump()
        return cls(**data)


class PutUsersMeRequest(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]

    class Config:
        from_attributes = True

    @classmethod
    def model_validate(cls, data):
        if isinstance(data, cls):
            data = data.model_dump()
        return cls(**data)


class PutUsersMeResponse(BaseModel):
    id: int
    email: EmailStr
    name: str

    class Config:
        from_attributes = True

    @classmethod
    def model_validate(cls, data):
        if isinstance(data, cls):
            data = data.model_dump()
        return cls(**data)


class User(BaseModel):
    id: int
    email: EmailStr
    name: str
    is_active: bool

    class Config:
        from_attributes = True

    @classmethod
    def model_validate(cls, data):
        if isinstance(data, cls):
            data = data.model_dump()
        return cls(**data)


class GetUsersResponse(BaseModel):
    users: List[User]

    class Config:
        from_attributes = True

    @classmethod
    def model_validate(cls, data):
        if isinstance(data, cls):
            data = data.model_dump()
        return cls(**data)


class GetUserResponse(BaseModel):
    id: int
    email: EmailStr
    name: str

    class Config:
        from_attributes = True

    @classmethod
    def model_validate(cls, data):
        if isinstance(data, cls):
            data = data.model_dump()
        return cls(**data)


class PutUserRequest(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]

    class Config:
        from_attributes = True

    @classmethod
    def model_validate(cls, data):
        if isinstance(data, cls):
            data = data.model_dump()
        return cls(**data)


class PutUserResponse(BaseModel):
    id: int
    email: EmailStr
    name: str

    class Config:
        from_attributes = True

    @classmethod
    def model_validate(cls, data):
        if isinstance(data, cls):
            data = data.model_dump()
        return cls(**data)


class DeleteUserResponse(BaseModel):
    id: int
    email: EmailStr
    name: str

    class Config:
        from_attributes = True

    @classmethod
    def model_validate(cls, data):
        if isinstance(data, cls):
            data = data.model_dump()
        return cls(**data)
