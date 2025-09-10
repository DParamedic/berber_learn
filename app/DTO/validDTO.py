from pydantic import BaseModel, ConfigDict

class Valid_Language(BaseModel):
    main_language: str
    translation_language: str

    model_config = ConfigDict(from_attributes=True)

class Valid_Dictionary(BaseModel):
    user_id: int
    language_id: int
    interval_list_id: int

    model_config = ConfigDict(from_attributes=True)

class Valid_Word(BaseModel):
    content: str

    model_config = ConfigDict(from_attributes=True)

class Valid_Word_Translate(BaseModel):
    word_id: int
    translate_ids: list[int]
    note_id: int | None = None
    dictionary_id: int
    interval_id: int
    count: int = 0

    model_config = ConfigDict(from_attributes=True)

class Valid_User(BaseModel):
    name: str | None = None
    telegram_id: int

    model_config = ConfigDict(from_attributes=True)

class Valid_Language(BaseModel):
    main_language: str
    translation_language: str

    model_config = ConfigDict(from_attributes=True)

class Valid_Dictionary(BaseModel):
    user_id: int
    language_id: int
    interval_list_id: int
    
class Valid_Word(BaseModel):
    content: str

    model_config = ConfigDict(from_attributes=True)

class Valid_Word_Translate(BaseModel):
    word_id: int
    translate_ids: list[int]
    note_id: int | None = None
    dictionary_id: int
    interval_id: int
    count: int = 0

    model_config = ConfigDict(from_attributes=True)

class Valid_Interval(BaseModel):
    length: int
    
class Valid_Interval_List(BaseModel):
    name: str

    model_config = ConfigDict(from_attributes=True)

class Valid_Link_Interval_List(BaseModel):
    interval_id: int
    interval_list_id: int

    model_config = ConfigDict(from_attributes=True)

class Valid_User_Settings(BaseModel):
    user_id: int
    interval_list_id: int

    model_config = ConfigDict(from_attributes=True)
