from typing import ClassVar, List

from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings
from sqlalchemy.ext.declarative import declarative_base

class Settings(BaseSettings):
    """
    Configurações gerais usadas na aplicação
    """
    API_V1_STR: str = '/api/v1'
    DB_URL: str = 'postgresql+asyncpg://geek:university@localhost:5432/faculdade'
    DBBaseModel: ClassVar = declarative_base()

    class Config:
        case_sensitive = True

settings = Settings()