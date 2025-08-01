from sqlalchemy import ForeignKey, UniqueConstraint, PrimaryKeyConstraint, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base, varchar255, varchar31, int8

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

class Dictionary(Base):
    """Модель для хранения словарей пользователя.

    Attributes:
        id (int): уникальный идентификатор словаря
        user_id (int): id пользователя
        language_id (int): id языковой модели
    """
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id = mapped_column(ForeignKey("user.id", ondelete="cascade"))
    language_id = mapped_column(ForeignKey("language.id", ondelete="no action"))
    interval_list_id = mapped_column(ForeignKey("interval_list.id", ondelete="no action"))

    user = relationship("User", back_populates="dictionaries", uselist=False)
    language: Mapped["Language"] = relationship(back_populates="dictionaries", uselist=False)
    
    word_translate: Mapped["Word_Translate"] = relationship(back_populates="dictionary")

    __table_args__ = (
        UniqueConstraint("user_id", "language_id", name="uq_user_id_language_id"),
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
    
    dictionaries: Mapped["Dictionary"] = relationship(back_populates="language", uselist=False)

class Word(Base):
    """Модель для хранения слов или переводов.

    Attributes:
        id (int): уникальный идентификатор слова
        content (str): содержимое слова
    """
    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[varchar31] = mapped_column(index=True)

    word_association: Mapped[list["Word_Translate"]] = relationship(
        foreign_keys="[Word_Translate.word_id]",
        back_populates="words",
        )
    translations_association: Mapped[list["Word_Translate"]] = relationship(
        foreign_keys="[Word_Translate.translate_id]",
        back_populates="translations",
        )
    
class Note(Base):
    """Модель для хранения заметок.

    Attributes:
        id (int): уникальный идентификатор заметки
        content (str): содержимое заметки
    """
    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[varchar255]

    word_translate: Mapped["Word_Translate"] = relationship(back_populates="note", uselist=False)
    
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
    dictionary_id = mapped_column(ForeignKey("dictionary.id", ondelete="cascade"))
    word_id = mapped_column(ForeignKey("word.id", ondelete="cascade"))
    translate_id = mapped_column(
        ForeignKey("word.id", ondelete="cascade"),
        CheckConstraint("translate_id != word_id", name="check_translate_id_word_id"),
        )
    note_id: Mapped[int | None] = mapped_column(ForeignKey("note.id", ondelete="cascade"))
    interval_id = mapped_column(ForeignKey("interval.id"))
    count: Mapped[int]
    
    dictionary: Mapped["Dictionary"] = relationship(back_populates="word_translate", uselist=False)
    words: Mapped[list["Word"]] = relationship(
        foreign_keys=[word_id],
        back_populates="word_association",
        )
    translations: Mapped[list["Word"]] = relationship(
        foreign_keys=[translate_id],
        back_populates="translations_association"
        )
    note: Mapped["Note"] = relationship(back_populates="word_translate", uselist=False)
    interval = relationship("Interval", back_populates="word_translates", uselist=False)

    __table_args__ = (
        PrimaryKeyConstraint(
            "dictionary_id",
            "word_id",
            "translate_id",
            name="pk_dictionary_id_word_id_translate_id"
            ),
    )

class Interval(Base):
    """Модель для хранения продолжительности интервалов.

    Attributes:
        id (int): Уникальный идентификатор интервала
        length (int): Длительность интервала
    """
    id: Mapped[int] = mapped_column(primary_key=True)
    length: Mapped[int] = mapped_column(unique=True)
    
    link_interval_lists: Mapped['Link_Interval_List'] = relationship(back_populates='interval')
    word_translates = relationship('Word_Translate', back_populates='interval')

class Interval_List(Base):
    """Модель для хранения списков интервалов.
    
    Attributes:
        id (int): Уникальный идентификатор списка
        name (str): Наименование списка

    Rules:
        1. Базовый -- classic.
        2. Если нет причин, то остальные -- m<n>, где n := 1,2...inf
    """
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[varchar31] = mapped_column(unique=True)

    link_interval_lists: Mapped['Link_Interval_List'] = relationship(back_populates='interval_list')

class Link_Interval_List(Base):
    """Модель для связи списков с их интервалами.

    Attributes:
        book_id (int): id списка
        length_id (int): id интервала
    """
    interval_id = mapped_column(ForeignKey('interval.id', ondelete='cascade'))
    interval_list_id = mapped_column(ForeignKey('interval_list.id', ondelete='cascade'))
    
    interval_list: Mapped['Interval_List'] = relationship(back_populates='link_interval_lists')
    interval: Mapped['Interval'] = relationship(back_populates='link_interval_lists')
    
    __table_args__ = (
        PrimaryKeyConstraint('interval_list_id', 'interval_id', name='pk_interval_list_id_interval_id'),
    )
