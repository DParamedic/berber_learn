from sqlalchemy import create_engine

from app.database import Base
from app.config import settings

engine = create_engine(f'mysql+pymysql://{settings.ADMIN_USER_NAME}:{settings.ADMIN_USER_PASSWORD}@localhost:3306/berber_learn', echo=True)

Base.metadata.create_all(engine)