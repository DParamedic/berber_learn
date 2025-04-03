from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import create_engine, Table

from db.database import (
    Base,
    Users,
    Dictionaries,
    Pages,
    Words,
)

from config import settings

engine = create_engine(settings.get_db_url)

with Session(engine) as session:
    pass

def insert_user(telegram_id: int) -> Users:
    user = Users(telegram_id=telegram_id)
    return user


new_word: str = 'Hellow'
new_word_tr = 'Привет'
new_word_tr2 = 'Здраствуй'
new_notes = 'аааааааааааааааааааааааааа'

user = Users(telegram_id=settings.ADMIN_ID)
dictionaries = Dictionaries(user_id=user.id)
pages = Pages(dict_id=dictionaries.id, name=0)
word = Words(
    dict_id=dictionaries.id,
    page_id=pages.id,
    word=new_word,
    translate=new_word_tr,
    translate_2=new_word_tr2,
    notes=new_notes,
    count=0,
    add_date=datetime.now(),
)
