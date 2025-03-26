from sqlalchemy import create_engine

from db.database import Base
from config import settings

def base_create():
    engine = create_engine(settings.get_db_url)
    Base.metadata.create_all(engine)