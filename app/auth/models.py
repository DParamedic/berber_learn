from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import int8, varchar31

from app.settings.models import User_Settings
from app.dictionary.models import Dictionary

class User('Base'):
    """
    Модель для хранения информации о пользователях.

    Attributes:
        id (int): уникальный идентификатор пользователя
        name (varchar31): имя пользователя
        telegram_id (int8): telegram id
    """
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[varchar31 | None]
    telegram_id: Mapped[int8]
    
    dictionaries: Mapped['Dictionary'] = relationship(back_populates='user')
    users_settings: Mapped['User_Settings'] = relationship(back_populates='user')
