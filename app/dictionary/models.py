from sqlalchemy import ForeignKey, UniqueConstraint, PrimaryKeyConstraint, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import varchar255, varchar31
from app.auth.models import User
from app.settings.models import Page

class Language('Base'):
    """
    Модель для хранения списка используемых языков

    Attributes:
        id (int): уникальный идентификатор языка
        name (str): название языка
    """
    id: Mapped[int] = mapped_column(primary_key=True)
    main_language: Mapped[varchar31]
    translation_language: Mapped[varchar31]
    
    dictionaries: Mapped['Dictionary'] = relationship(back_populates='language', uselist=False)

class Dictionary('Base'):
    """
    Модель для хранения словарей пользователя

    Attributes:
        id (int): уникальный идентификатор словаря
        user_id (int): id пользователя
    """
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id = mapped_column(ForeignKey('user.id', ondelete='cascade'))
    language_id = mapped_column(ForeignKey('language.id', ondelete='no action'))
    
    users: Mapped['User'] = relationship(back_populates='dictionary')
    languages: Mapped['Language'] = relationship(back_populates='dictionary', uselist=False)
    
    words: Mapped['Word'] = relationship(back_populates='dictionary')

    __table_args__ = (
        UniqueConstraint('language_id', 'user_id', name='dictionary_user_id_language_id_key'),
    )

class Word('Base'):
    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[varchar31] = mapped_column(index=True)
    
    word_translations: Mapped['Word_Translate'] = relationship(back_populates='word')
    
class Translate('Base'):
    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[varchar31] = mapped_column(index=True)

    word_translations: Mapped['Word_Translate'] = relationship(back_populates='translate')

class Note('Base'):
    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[varchar255]

    word_translations: Mapped['Word_Translate'] = relationship(back_populates='note')
    
class Word_Translate('Base'):
    word_id = mapped_column(ForeignKey('word.id', ondelete='cascade'))
    translate_id = mapped_column(ForeignKey('translate.id', ondelete='cascade'))
    note_id: Mapped[int | None] = mapped_column(ForeignKey('note.id', ondelete='restrict'))
    dict_id = mapped_column(ForeignKey('dictionary.id', ondelete='cascade'))
    page_value = mapped_column(ForeignKey('page.id'))
    count: Mapped[int] = mapped_column(CheckConstraint('count < page_value', name='check_count_less_page'))
    
    words: Mapped['Word'] = relationship(back_populates='word_translate')
    translations: Mapped['Translate'] = relationship(back_populates='word_translate')
    notes: Mapped['Note'] = relationship(back_populates='word_translate')
    dictionaries: Mapped['Dictionary'] = relationship(back_populates='word_translate')
    pages: Mapped['Page'] = relationship(back_populates='word_translate')

    __table_args__ = (
        PrimaryKeyConstraint('word_id', 'dict_id', name='word_id_dict_id_primary_key')
    )


