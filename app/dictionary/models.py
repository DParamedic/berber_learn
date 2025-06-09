from sqlalchemy import ForeignKey, UniqueConstraint, PrimaryKeyConstraint, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base, varchar255, varchar31

class Dictionary(Base):
    """Модель для хранения словарей пользователя.

    Attributes:
        id (int): уникальный идентификатор словаря
        user_id (int): id пользователя
        language_id (int): id языковой модели
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
    """Модель для хранения списка пар языков, применяемых при идентификации словаря.

    Attributes:
        id (int): уникальный идентификатор языка
        main_language (str): название основного языка
        translation_language (str): название языка переводов
    """
    id: Mapped[int] = mapped_column(primary_key=True)
    main_language: Mapped[varchar31]
    translation_language: Mapped[varchar31]
    
    dictionaries: Mapped['Dictionary'] = relationship(back_populates='language', uselist=False)

class Word(Base):
    """Модель для хранения слов или переводов.

    Attributes:
        id (int): уникальный идентификатор слова
        content (str): содержимое слова
    """
    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[varchar31] = mapped_column(index=True)
    
    word_association: Mapped[list['Word_Translate']] = relationship(back_populates='word')
    translations_association: Mapped[list['Word_Translate']] = relationship(back_populates='word')
    
class Note(Base):
    """Модель для хранения заметок.

    Attributes:
        id (int): уникальный идентификатор заметки
        content (str): содержимое заметки
    """
    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[varchar255]

    word_translate: Mapped['Word_Translate'] = relationship(back_populates='note', uselist=False)
    word_translations: Mapped['Word_Translate'] = relationship(back_populates='note')
    
class Word_Translate(Base):
    """Модель для связи слова с его переводом/переводами.

    Attributes:
        word_id (int): id слова
        translate_id (int): id перевода
        note_id (int): id заметки
        dict_id (int): id словаря
        page_id (int): id длительности пребывания слова в таблице
        count (int): длительность пребывания по слова в page по факту
    """
    word_id = mapped_column(ForeignKey('word.id', ondelete='cascade'))
    translate_id = mapped_column(
        ForeignKey(
            'word.id', ondelete='cascade'
            ),CheckConstraint(
                'second_word_id != word_id',
                name='check_second_word_id_not_eq_word_id'
                )
            )
    note_id: Mapped[int | None] = mapped_column(
        ForeignKey('note.id', ondelete='restrict')
        )
    dict_id = mapped_column(ForeignKey('dictionary.id', ondelete='cascade'))
    page_id = mapped_column(ForeignKey('page.id'))
    count: Mapped[int] = mapped_column(
        CheckConstraint('count < page_value', name='check_count_less_page')
        )
    
    dictionary: Mapped['Dictionary'] = relationship(
        back_populates='word_translate', uselist=False)
    words: Mapped[list['Word']] = relationship(
        back_populates='word_association')
    translations: Mapped[list['Word']] = relationship(
        back_populates='translations_association')
    note: Mapped['Note'] = relationship(
        back_populates='word_translate', uselist=False)
    page = relationship(
        'Page', back_populates='word_translates', uselist=False)

    __table_args__ = (
        PrimaryKeyConstraint(
            'word_id',
            'dict_id',
            'translate_id',
            name='word_id_dict_id_primary_key'
            ),
    )


