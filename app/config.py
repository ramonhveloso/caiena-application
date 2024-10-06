from pydantic import AnyUrl, BaseModel


class Environment(BaseModel):
    OPEN_WEATHER_URL: AnyUrl
    DATABASE_URL: str
    TEST_DATABASE_URL: str
    SECRET_KEY: str
    SECRET_KEY_GITHUB: str
    SECRET_KEY_OPEN_WEATHER: str
    SMTP_SERVER: str
    SMTP_PORT: int
    SMTP_USERNAME: str
    SMTP_PASSWORD: str
    
