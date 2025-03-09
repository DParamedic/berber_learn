import datetime

from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
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
        Date: DATE
    }
