from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base, int8, varchar31

class User(Base):
    """
    Модель для хранения информации о пользователях.

    Attributes:
        id (int | None): уникальный идентификатор пользователя
        name (varchar31): имя пользователя
        telegram_id (int8): telegram id
    """
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[varchar31 | None]
    telegram_id: Mapped[int8] = mapped_column(unique=True)
    
    dictionaries = relationship('Dictionary', back_populates='user')
    user_settings = relationship('User_Settings', back_populates='user', uselist=False)
