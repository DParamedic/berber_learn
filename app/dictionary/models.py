from sqlalchemy import ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base, varchar255, varchar31
from app.auth.models import User

class Dictionary(Base):
    """
    Модель для хранения словарей пользователя

    Attributes:
        id (int): уникальный идентификатор словаря
        user_id (int): id пользователя
    """
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id = mapped_column(ForeignKey('user.id', ondelete='cascade'))
    language_id = mapped_column(ForeignKey('language.id', ondelete='no action'))
    
    users: Mapped[User] = relationship(back_populates='dictionary')
    words: Mapped['Word'] = relationship(back_populates='dictionary')
    languages: Mapped['Language'] = relationship(back_populates='dictionary', uselist=False)

    __table_args__ = (
        UniqueConstraint('language_id', 'user_id', name='dictionary_user_id_language_id_key'),
    )

class Language(Base):
    """
    Модель для хранения списка используемых языков

    Attributes:
        id (int): уникальный идентификатор языка
        name (str): название языка
    """
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[varchar31]
    
    dictionaries: Mapped[Dictionary] = relationship(back_populates='language', uselist=False)

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
        note (varchar225): заметка
        page_value (int): продолжительность нахождения на 'странице'
        count (int): счетчик продолжительности нахождения на странице
    """
    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[varchar31]
    translate_id = mapped_column(ForeignKey('translate.id', ondelete='restrict'))
    note_id: Mapped[int | None] = mapped_column(ForeignKey('note.id', ondelete='restrict'))
    dict_id = mapped_column(ForeignKey('dictionary.id', ondelete='cascade'))
    page_value: Mapped[int]
    count: Mapped[int]
    
    dictionaries: Mapped[Dictionary] = relationship(back_populates='word')
    translate: Mapped['Translate'] = relationship(back_populates='word')
    notes: Mapped['Note'] = relationship(back_populates='word', uselist=False)
    
    __table_args__ = (
        UniqueConstraint('dict_id', 'content', name='word_content_dict_id_key'),
        Index('dict_id_content_idx', 'dict_id', 'content'),
    )

class Translate(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[varchar31] = mapped_column(index=True)

    words: Mapped[Word] = relationship(back_populates='translate')

class Note(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[varchar255]
    
    words: Mapped[Word] = relationship(back_populates='note', uselist=False)

