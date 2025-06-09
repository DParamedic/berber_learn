from sqlalchemy import ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base, varchar31

class Page(Base):
    """Модель для хранения продолжительности интервалов.

    Attributes:
        id (int): Уникальный идентификатор интервала
        length (int): Длительность интервала
    """
    # Interval
    id: Mapped[int] = mapped_column(primary_key=True)
    length: Mapped[int] = mapped_column(unique=True)
    
    page_books: Mapped['Page_Book'] = relationship(back_populates='page')
    word_translates = relationship('Word_Translate', back_populates='page')

class Book(Base):
    """Модель для хранения списков интервалов.
    
    Attributes:
        id (int): Уникальный идентификатор списка
        name (str): Наименование списка

    Rules:
        1. Базовый -- classic.
        2. Если нет причин, то остальные -- m<N>, где N := 1,2...inf
    """
    # List
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[varchar31] = mapped_column(unique=True)

    page_books: Mapped['Page_Book'] = relationship(back_populates='book')
    users_settings: Mapped['User_Settings'] = relationship(back_populates='page')

class Page_Book(Base):
    """Модель для связи списков с их интервалами.

    Attributes:
        book_id (int): id списка
        length_id (int): id интервала
    """
    # Interval_List
    book_id = mapped_column(ForeignKey('book.id', ondelete='cascade'))
    length_id = mapped_column(ForeignKey('page.id', ondelete='cascade'))
    
    books: Mapped['Book'] = relationship(back_populates='page_book')
    pages: Mapped['Page'] = relationship(back_populates='page_book')
    
    __table_args__ = (
        PrimaryKeyConstraint('book_id', 'length_id', name='book_id_length_id_primary_key'),
    )
class User_Settings(Base):
    """Модель для хранения пользовательских настроек.
    
    Attributes:
        user_id (int): id пользователя
        book_id (int): id списка
    """
    user_id = mapped_column(ForeignKey('user.id', ondelete='cascade'))
    book_id = mapped_column(ForeignKey('book.id', ondelete='cascade'))

    user = relationship('User', back_populates='user_settings', uselist=False)
    book: Mapped['Book'] = relationship(back_populates='user_settings', uselist=False)

    __table_args__ = (
        PrimaryKeyConstraint('user_id', 'book_id', name='user_id_book_id_primary_key'),
    )