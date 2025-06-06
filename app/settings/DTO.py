from pydantic import BaseModel, ConfigDict

from app.auth.DTO import User

class Page(BaseModel):
    length: int
    
    model_config = ConfigDict(from_attributes=True)
    
class Book(BaseModel):
    name: str

    model_config = ConfigDict(from_attributes=True)
    
class Page_Book(BaseModel):
    books: list[Book]
    pages: list[Page]
    
    model_config = ConfigDict(from_attributes=True)
    
class User_Settings(BaseModel):
    user: User
    book: Book
    
    model_config = ConfigDict(from_attributes=True)
    