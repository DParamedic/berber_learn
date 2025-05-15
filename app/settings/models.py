from sqlalchemy import ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import varchar31
from app.auth.models import User

class Page('Base'):
    id: Mapped[int] = mapped_column(primary_key=True)
    length: Mapped[int] = mapped_column(unique=True)
    
    page_books: Mapped['Page_Book'] = relationship(back_populates='page')

class Book('Base'):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[varchar31] = mapped_column(unique=True)
    
    page_books: Mapped['Page_Book'] = relationship(back_populates='book')
    users_settings: Mapped['User_Settings'] = relationship(back_populates='page')
    
class Page_Book('Base'):
    book_id = mapped_column(ForeignKey('book.id', ondelete='cascade'))
    length_id = mapped_column(ForeignKey('page.id', ondelete='cascade'))
    
    books: Mapped['Book'] = relationship(back_populates='page_book')
    pages: Mapped['Page'] = relationship(back_populates='page_book')
    
    __table_args__ = (
        PrimaryKeyConstraint('book_id', 'length_id', name='book_id_length_id_primary_key')
    )
class User_Settings('Base'):
    user_id = mapped_column(ForeignKey('user.id', ondelete='cascade'))
    book_id = mapped_column(ForeignKey('book.id', ondelete='cascade'))

    books: Mapped['User'] = relationship(back_populates='user_settings')
    pages: Mapped['Book'] = relationship(back_populates='user_settings')

    __table_args__ = (
        PrimaryKeyConstraint('user_id', 'book_id', name='user_id_book_id_primary_key')
    )