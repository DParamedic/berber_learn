from sqlalchemy import ForeignKey, UniqueConstraint, PrimaryKeyConstraint, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base, varchar255, varchar31

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
    
    user = relationship('User', back_populates='dictionary', uselist=False)
    language: Mapped['Language'] = relationship(back_populates='dictionary', uselist=False)
    
    word_translate: Mapped['Word_Translate'] = relationship(back_populates='dictionary')

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
    main_language: Mapped[varchar31]
    translation_language: Mapped[varchar31]
    
    dictionary: Mapped['Dictionary'] = relationship(back_populates='language', uselist=False)

class Word(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[varchar31] = mapped_column(index=True)
    
    word_association: Mapped[list['Word_Translate']] = relationship(back_populates='word')
    translations_association: Mapped[list['Word_Translate']] = relationship(back_populates='word')
    
class Note(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[varchar255]

    word_translate: Mapped['Word_Translate'] = relationship(back_populates='note', uselist=False)
    
class Word_Translate(Base):
    word_id = mapped_column(ForeignKey('word.id', ondelete='cascade'))
    translate_id = mapped_column(ForeignKey('word.id', ondelete='cascade'),
                                   CheckConstraint('second_word_id != word_id', name='check_second_word_id_not_eq_word_id'))
    note_id: Mapped[int | None] = mapped_column(ForeignKey('note.id', ondelete='restrict'))
    dict_id = mapped_column(ForeignKey('dictionary.id', ondelete='cascade'))
    page_id = mapped_column(ForeignKey('page.id'))
    count: Mapped[int] = mapped_column(CheckConstraint('count < page_value', name='check_count_less_page'))
    
    dictionary: Mapped['Dictionary'] = relationship(back_populates='word_translate', uselist=False)
    words: Mapped[list['Word']] = relationship(back_populates='word_association')
    translations: Mapped[list['Word']] = relationship(back_populates='translations_association')
    note: Mapped['Note'] = relationship(back_populates='word_translate', uselist=False)
    page = relationship('Page', back_populates='word_translates', uselist=False)

    __table_args__ = (
        PrimaryKeyConstraint('word_id', 'dict_id', 'translate_id', name='word_id_dict_id_primary_key'),
    )


