from pydantic import ConfigDict

from app.DTO import (
    Valid_Dictionary,
    Valid_Language,
    Valid_Word,
    Valid_Word_Translate,
)

class Extra_Language(Valid_Language):
    model_config = ConfigDict(extra="allow")
    def validate(self) -> Valid_Language:
        return Valid_Language(**self.model_dump())

class Extra_Dictionary(Valid_Dictionary):
    model_config = ConfigDict(extra="allow")
    def validate(self) -> Valid_Dictionary:
        return Valid_Dictionary(**self.model_dump())

class Extra_Word(Valid_Word):
    model_config = ConfigDict(extra="allow")
    def validate(self) -> Valid_Word:
        return Valid_Word(**self.model_dump())

class Extra_Word_Translate(Valid_Word_Translate):
    model_config = ConfigDict(extra="allow")
    def validate(self) -> Valid_Word_Translate:
        return Valid_Word_Translate(**self.model_dump())
