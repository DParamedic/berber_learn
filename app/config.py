from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    DB_PROVIDER: str = "postgresql+asyncpg"

    TELEGRAM_BOT_TOKEN: str
    TELEGRAM_ADMIN_ID: int
    URL_SERVER: str
    
    class Config:
        env_file = '.env'
        env_file_encoding = "utf-8"
        extra = 'ignore'

    @property
    def get_db_url(self) -> str:
        return f'{self.DB_PROVIDER}://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}'
    
settings = Settings()