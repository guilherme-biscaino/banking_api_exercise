from pydantic import Field
from pydantic_settings import BaseSettings
from env import DATABASE_DEV_URL


class Settings(BaseSettings):
    DB_URL: str = Field(default=DATABASE_DEV_URL)


settings = Settings()
