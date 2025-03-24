import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    ADMIN_USER_NAME_FOR_DB: str
    ADMIN_USER_PASSWORD_FOR_DB: str
    BOT_TOKEN: str
    ADMIN_ID: int
    URL_SERVER: str
    
    class Config:
        env_file = '.env'
        env_file_encoding = "utf-8"
        validate_default = False # Изменить
        extra = 'ignore'

    @property
    def get_db_url(self) -> str:
        """Возвращает имя администратора."""
        return f'mysql://{self.ADMIN_USER_NAME_FOR_DB}:{self.ADMIN_USER_PASSWORD_FOR_DB}@localhost:3306' # /berber_learn для запросов
    
settings = Settings()