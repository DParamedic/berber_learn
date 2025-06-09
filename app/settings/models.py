from sqlalchemy import ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base, varchar31

class Interval(Base):
    """Модель для хранения продолжительности интервалов.

    Attributes:
        id (int): Уникальный идентификатор интервала
        length (int): Длительность интервала
    """
    id: Mapped[int] = mapped_column(primary_key=True)
    length: Mapped[int] = mapped_column(unique=True)
    
    page_books: Mapped['Link_Interval_List'] = relationship(back_populates='interval')
    word_translates = relationship('Word_Translate', back_populates='interval')

class Interval_List(Base):
    """Модель для хранения списков интервалов.
    
    Attributes:
        id (int): Уникальный идентификатор списка
        name (str): Наименование списка

    Rules:
        1. Базовый -- classic.
        2. Если нет причин, то остальные -- m<N>, где N := 1,2...inf
    """
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[varchar31] = mapped_column(unique=True)

    page_books: Mapped['Link_Interval_List'] = relationship(back_populates='interval_list')
    users_settings: Mapped['User_Settings'] = relationship(back_populates='interval_list')

class Link_Interval_List(Base):
    """Модель для связи списков с их интервалами.

    Attributes:
        book_id (int): id списка
        length_id (int): id интервала
    """
    # link_interval_list
    interval_list_id = mapped_column(ForeignKey('interval_list.id', ondelete='cascade'))
    interval_id = mapped_column(ForeignKey('interval.id', ondelete='cascade'))
    
    books: Mapped['Interval_List'] = relationship(back_populates='link_interval_list')
    pages: Mapped['Interval'] = relationship(back_populates='link_interval_list')
    
    __table_args__ = (
        PrimaryKeyConstraint('interval_list_id', 'interval_id', name='pk_interval_list_id_interval_id'),
    )
class User_Settings(Base):
    """Модель для хранения пользовательских настроек.
    
    Attributes:
        user_id (int): id пользователя
        book_id (int): id списка
    """
    user_id = mapped_column(ForeignKey('user.id', ondelete='cascade'))
    interval_list_id = mapped_column(ForeignKey('interval_list.id', ondelete='cascade'))

    user = relationship('User', back_populates='user_settings', uselist=False)
    book: Mapped['Interval_List'] = relationship(back_populates='user_settings', uselist=False)

    __table_args__ = (
        PrimaryKeyConstraint('user_id', 'interval_list_id', name='pk_user_id_interval_list_id'),
    )