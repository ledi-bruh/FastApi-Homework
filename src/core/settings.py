from pydantic import BaseSettings, Field
from utils.pattern import singleton


@singleton
class Settings(BaseSettings):
    host: str = 'localhost'
    port: int = 9999
    
    db_login: str
    db_password: str
    db_host: str
    db_port: int
    db_database: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()