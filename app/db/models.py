from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base, int8, varchar255, varchar31

class User(Base):
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
    
    dictionaries = relationship('Dictionary', back_populates='user')
    
class Dictionary(Base):
    """
    Модель для хранения словарей пользователя

    Attributes:
        id (int): уникальный идентификатор словаря
        user_id (int): id пользователя
    """
    id: Mapped[int] = mapped_column(primary_key=True)
    language_id: Mapped[int]
    user_id = mapped_column(ForeignKey('users.id', ondelete='cascade'))
    
    users = relationship('User', back_populates='dictionary')
    words = relationship('Word', back_populates='dictionary')
    languages = relationship('Language', back_populates='dictionary')

class Language(Base):
    """
    Модель для хранения списка используемых языков

    Attributes:
        id (int): уникальный идентификатор языка
        name (str): название языка
    """

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[varchar31]
    
    dictionaries = relationship('Dictionary', back_populates='language')

class Word(Base):
    """
    Модель для хранения слов

    Attributes:
        id (int): уникальный идентификатор слова
        dict_id (int): id словаря
        name (varchar31): слово
        translate (varchar31): перевод слова
        translate_2 (varchar31): перевод слова 2
        translate_3 (varchar31): перевод слова 3
        notes (varchar225): заметка
        page_value (int): продолжительность нахождения на 'странице'
        count (int): счетчик продолжительности нахождения на странице
    """
    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[varchar31] = mapped_column(index=True)
    dict_id = mapped_column(ForeignKey('dictionaries.id', ondelete='cascade'))
    page_value: Mapped[int]
    count: Mapped[int]
    
    dictionaries = relationship('Dictionary', back_populates='word')
    translate = relationship('Translate', back_populates='word')
    notes = relationship('Notes', back_populates='word')
    
    __table_args__ = (
        UniqueConstraint('dict_id', 'word', name='word_content_dict_id_key'),
    )

class Translate(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[varchar31] = mapped_column(index=True)
    word_id = mapped_column(ForeignKey('word.id', ondelete='cascade'))

    words = relationship('Word', back_populates='translate')

class Notes(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[varchar255]
    word_id = mapped_column(ForeignKey('word.id', ondelete='cascade'))
    
    words = relationship('Word', back_populates='note')

