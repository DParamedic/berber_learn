from asyncio import run

from app.main import start_base
from app.database import Base
from app.auth.models import User
from app.dictionary.models import Dictionary, Language, Word, Translate, Note, Word_Translate
from app.settings.models import Page, Book, Page_Book, User_Settings

if __name__ == '__main__':
    run(start_base())
    print(Base.metadata.tables)