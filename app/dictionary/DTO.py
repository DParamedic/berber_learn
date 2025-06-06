from pydantic import BaseModel, ConfigDict

class Word(BaseModel):
    content: str

    model_config = ConfigDict(from_attributes=True)

class Note(BaseModel):
    content: str

    model_config = ConfigDict(from_attributes=True)

class Word_Translate(BaseModel):
    word: Word
    translates: list[Word]
    note: Note | None = None
    dictionary_id: int
    page_id: int
    count: int = 0
    
    model_config = ConfigDict(from_attributes=True)
