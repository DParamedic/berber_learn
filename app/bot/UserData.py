from app.DTO import (
    Extra_Dictionary,
    Extra_Language,
    Extra_Word,
    Extra_Word_Translate,
)

class UserData:
    def __init__(self):
        self._dictionary: Extra_Dictionary|None = None
        self._word: Extra_Word|None = None
        self._old_word: Extra_Word|None = None
        self._note: Extra_Word|None = None
        self._word_translate: Extra_Word_Translate|None = None
        self._translates: list[Extra_Word]|None = None
        self._dictionary_ids: list[int]|None = None
        self._interval_ids: list[int]|None = None
        self._language: Extra_Language|None = None

    @property
    def dictionary(self):
        return self._dictionary
    @dictionary.setter
    def dictionary(self, other: Extra_Dictionary):
        self._dictionary = Extra_Dictionary.model_construct(
            other.model_dump(other))
    @dictionary.deleter
    def dictionary(self):
        print("Этот объект не предназначен для удаления.")

    def set_dictionary(self, **kwargs):
        if not isinstance(self._dictionary, Extra_Dictionary):
            self._dictionary = Extra_Dictionary.model_construct()
        for attr, value in kwargs.items():
            setattr(self._dictionary, attr, value)

    @property
    def word(self):
        return self._word
    @word.setter
    def word(self, other: Extra_Word):
        self._word = Extra_Word.model_construct(
            **other.model_dump())
    @word.deleter
    def word(self):
        self._word = None

    def set_word(self, **kwargs):
        if not isinstance(self._word, Extra_Word):
            self._word = Extra_Word.model_construct()
        for attr, value in kwargs.items():
            setattr(self._word, attr, value)

    @property
    def old_word(self):
        return self._old_word
    @old_word.setter
    def old_word(self, other: Extra_Word):
        self._old_word = Extra_Word.model_construct(
            **other.model_dump())
    @old_word.deleter
    def old_word(self):
        self._old_word = None

    def set_old_word(self, **kwargs):
        if not isinstance(self._old_word, Extra_Word):
            self._old_word = Extra_Word.model_construct()
        for attr, value in kwargs.items():
            setattr(self._old_word, attr, value)

    @property
    def note(self):
        return self._note
    @note.setter
    def note(self, other: Extra_Word):
        self._note = Extra_Word.model_construct(
            **other.model_dump())
    @note.deleter
    def note(self):
        self._note = None

    def set_note(self, **kwargs):
        if not isinstance(self._note, Extra_Word):
            self._note = Extra_Word.model_construct()
        for attr, value in kwargs.items():
            setattr(self._note, attr, value)

    @property
    def word_translate(self):
        return self._word_translate
    @word_translate.setter
    def word_translate(self, other: Extra_Word_Translate):
        self._word_translate = Extra_Word_Translate.model_construct(
            **other.model_dump())
    @word_translate.deleter
    def word_translate(self):
        self._word_translate = None

    def set_word_translate(self, **kwargs):
        if not isinstance(self._word_translate, Extra_Word_Translate):
            self._word_translate = Extra_Word_Translate.model_construct()
        for attr, value in kwargs.items():
            setattr(self._word_translate, attr, value)

    @property
    def translates(self):
        return self._translates
    @translates.setter
    def translates(self, _):
        ...
    @translates.deleter
    def translates(self):
        self._translates = None

    @property
    def translates_ids(self) -> list[int]:
        if self._translates:
            return [translate.id for translate in self._translates]
        else:
            return None
    @translates_ids.setter
    def translates_ids(self, ids: list[int]):
        if not self._translates:
            self._translates = [
                Extra_Word.model_construct(
                    id=id,
                ) for id in ids
            ]
        else:
            assert len(ids) == len(self._translates), "Необходимы списки одинаковой длины!"
            for idx, translate in enumerate(self._translates):
                translate.id = ids[idx]
    
    @property
    def translates_contents(self) -> list[str]:
        if self._translates:
            return [translate.content for translate in self._translates]
        else:
            return None
    @translates_contents.setter
    def translates_contents(self, contents: list[int]):
        if not self._translates:
            self._translates = [
                Extra_Word.model_construct(
                    content=content,
                ) for content in contents
            ]
        else:
            assert len(contents) == len(self._translates), "Необходимы списки одинаковой длины!"
            for idx, translate in enumerate(self._translates):
                translate.content = contents[idx]

    @property
    def valid_translates(self) -> list[Extra_Word]|list:
        translates = []
        if self._translates:
            for translate in self._translates:
                translates.append(translate.validate())
        return translates
        
    @property
    def dictionary_ids(self):
        return self._dictionary_ids
    @dictionary_ids.setter
    def dictionary_ids(self, dictionary_ids: list[int]):
        if not isinstance(self._dictionary_ids, list):
            self._dictionary_ids = []
        for id in dictionary_ids:
            self._dictionary_ids.append(id)
    @dictionary_ids.deleter
    def dictionary_ids(self):
        self._dictionary_ids = None
    
    @property
    def interval_ids(self):
        return self._interval_ids
    @interval_ids.setter
    def interval_ids(self, interval_ids: list[int]):
        if not isinstance(self._interval_ids, list):
            self._interval_ids = []
        for id in interval_ids:
            self._interval_ids.append(id)
    @interval_ids.deleter
    def interval_ids(self):
        self._interval_ids = None
    
    @property
    def language(self):
        return self._language
    @language.setter
    def language(self, other: Extra_Language):
        self._language = Extra_Language.model_construct(
            **other.model_dump())
    @language.deleter
    def language(self):
        self._language = None

    def set_language(self, **kwargs):
        if not isinstance(self._language, Extra_Language):
            self._language = Extra_Language.model_construct()
        for attr, value in kwargs.items():
            setattr(self._language, attr, value)

    def clear(self):
        self.__init__()