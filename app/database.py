from datetime import datetime

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, declared_attr, mapped_column, Mapped
from sqlalchemy import DateTime, text
from sqlalchemy.dialects.postgresql import BIGINT
from sqlalchemy import String

from app.config import settings

type int8 = int
type varchar31 = str
type varchar255 = str

engine = create_async_engine(
    settings.get_db_url,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    echo=False,
)

async_session_maker = async_sessionmaker(
    engine,
    expire_on_commit=False,
    )

class Base(DeclarativeBase):
    __abstract__ = True

    type_annotation_map = {
        int8: BIGINT,
        varchar31: String(31),
        varchar255: String(255),
    }
    
    @declared_attr
    def __tablename__(cls) -> str:
        """Имя таблицы по умолчанию — имя класса в нижнем регистре."""
        return cls.__name__.lower()
    
    @declared_attr
    def created_at(cls) -> Mapped[datetime]:
        """Время создания записи."""
        return mapped_column(
            DateTime,
            server_default=text("TIMEZONE('Asia/Tomsk', now())"),
            nullable=False,
        )
