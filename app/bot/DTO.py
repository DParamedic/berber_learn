from pydantic import ConfigDict

from app.dictionary.DTO import (
    Language as Base_Language,
    Dictionary as Base_Dictionary,
    Word as Base_Word,
    Word_Translate as Base_Word_Translate,
)

class Language(Base_Language):
    model_config = ConfigDict(extra="allow")
    def validate(self) -> Base_Language:
        return Base_Language.model_validate(self.model_dump())

class Dictionary(Base_Dictionary):
    model_config = ConfigDict(extra="allow")
    def validate(self) -> Base_Dictionary:
        return Base_Dictionary.model_validate(self.model_dump())

class Word(Base_Word):
    model_config = ConfigDict(extra="allow")
    def validate(self) -> Base_Word:
        return Base_Word.model_validate(self.model_dump())

class Word_Translate(Base_Word_Translate):
    model_config = ConfigDict(extra="allow")
    def validate(self) -> Base_Word_Translate:
        return Base_Word_Translate.model_validate(self.model_dump())
