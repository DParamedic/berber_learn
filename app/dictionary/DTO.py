from pydantic import BaseModel, ConfigDict

class Language(BaseModel):
    main_language: str
    translation_language: str
    
    model_config = ConfigDict(from_attributes=True)

class Dictionary(BaseModel):
    user_id: int
    language_id: int
    interval_list_id: int
    
    model_config = ConfigDict(from_attributes=True)
    
class Word(BaseModel):
    content: str

    model_config = ConfigDict(from_attributes=True)

class Note(BaseModel):
    content: str

    model_config = ConfigDict(from_attributes=True)

class Word_Translate(BaseModel):
    word_id: int
    translate_ids: list[int]
    note_id: int | None = None
    dictionary_id: int
    interval_id: int
    count: int = 0
    
    model_config = ConfigDict(from_attributes=True)
