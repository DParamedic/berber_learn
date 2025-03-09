import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ADMIN_USER_NAME: str
    ADMIN_USER_PASSWORD: str
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
    )

    def get_admin_user_name(self) -> str:
        """Возвращает имя администратора."""
        return self.ADMIN_USER_NAME
    
    def get_admin_user_password(self) -> str:
        """Возвращает пароль администратора."""
        return self.ADMIN_USER_PASSWORD


settings = Settings()