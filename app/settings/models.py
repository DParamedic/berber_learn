from sqlalchemy import ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base, varchar255, varchar31
from app.auth.models import User

class Page(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    length: Mapped[int]
    
class Book(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    
class Settings(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    book_id = mapped_column(ForeignKey('book.id', ondelete='cascade'))
    length_id = mapped_column(ForeignKey('page.id', ondelete='cascade'))