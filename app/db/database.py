import datetime

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.mysql import INTEGER, SMALLINT, DATE

type SmallIntUnsigned = int
type IntegerUnsigned = int
type Varchar_31 = str
type Varchar_255 = str
type Date = datetime.datetime

class Base(DeclarativeBase):
    type_annotation_map = {
        SmallIntUnsigned: SMALLINT(unsigned=True),
        IntegerUnsigned: INTEGER(unsigned=True),
        Varchar_31: String(31),
        Varchar_255: String(255),
        Date: DATE,
    }
    
class Users(Base):
    __tablename__ = 'users'
    
    id: Mapped[SmallIntUnsigned] = mapped_column(primary_key=True, autoincrement=True)
    telegram_id: Mapped[IntegerUnsigned]
    
class Dictionaries(Base):
    __tablename__ = 'dictionaries'
    
    id: Mapped[SmallIntUnsigned] = mapped_column(primary_key=True, autoincrement=True)
    user_id = mapped_column(ForeignKey('users.id', ondelete='cascade'))
    
class Pages(Base):
    __tablename__ = 'pages'
    
    id: Mapped[SmallIntUnsigned] = mapped_column(primary_key=True, autoincrement=True)
    dict_id = mapped_column(ForeignKey('dictionaries.id', ondelete='cascade'))
    page_name: Mapped[SmallIntUnsigned]
    
class Words(Base):
    __tablename__ = 'words'
    
    id: Mapped[SmallIntUnsigned] = mapped_column(primary_key=True, autoincrement=True)
    dict_id = mapped_column(ForeignKey('dictionaries.id', ondelete='cascade'))
    page_id = mapped_column(ForeignKey('pages.id'))
    word: Mapped[Varchar_31]
    translate: Mapped[Varchar_31]
    translate_2: Mapped[Varchar_31 | None]
    translate_3: Mapped[Varchar_31 | None]
    notes: Mapped[Varchar_31 | None]
    count: Mapped[SmallIntUnsigned]
    add_date: Mapped[Date]
