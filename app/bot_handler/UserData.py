from typing import Iterator, Generator

from app.models import Word_Translate
from app.DTO import (
    Extra_Dictionary,
    Extra_Language,
    Extra_Word,
    Extra_Word_Translate,
    TreePathANdContentView,
)

class UserData:
    def __init__(self):
        self._dictionary: Extra_Dictionary|None = None
        self._old_word: Extra_Word|None = None
        self._word: Extra_Word|None = None
        self._translations: list[Extra_Word]|None = None
        self._note: Extra_Word|None = None
        self._word_translate: Extra_Word_Translate|None = None
        self._language: Extra_Language|None = None
        self._dictionary_ids: list[int]|None = None
        self._interval_ids: list[int]|None = None
        self._word_translations_order: Generator[TreePathANdContentView, None, None]|None = None
        self._current_object: TreePathANdContentView|None = None
        self._current_dictionary: str|None = None
        self._current_word: str|None = None
        self._choice_count: int|None = None
        self._dialog_active: bool = False
        self._done_event: bool = False

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
            self._dictionary = Extra_Dictionary.model_construct(
                id = None,
                user_id = None,
                language_id = None,
                interval_list_id = None,
                language_represent = None,
            )
        for attr, value in kwargs.items():
            setattr(self._dictionary, attr, value)

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
    def translations(self):
        return self._translations
    @translations.setter
    def translations(self, _):
        ...
    @translations.deleter
    def translations(self):
        self._translations = None

    @property
    def translations_ids(self) -> list[int]:
        if self._translations:
            return [translate.id for translate in self._translations]
        else:
            return None
    @translations_ids.setter
    def translations_ids(self, ids: list[int]):
        if not self._translations:
            self._translations = [
                Extra_Word.model_construct(
                    id=id,
                ) for id in ids
            ]
        else:
            assert len(ids) == len(self._translations), "Необходимы списки одинаковой длины!"
            for idx, translate in enumerate(self._translations):
                translate.id = ids[idx]
    
    @property
    def translations_contents(self) -> list[str]:
        if self._translations:
            return [translate.content for translate in self._translations]
        else:
            return None
    @translations_contents.setter
    def translations_contents(self, contents: list[int]):
        if not self._translations:
            self._translations = [
                Extra_Word.model_construct(
                    content=content,
                ) for content in contents
            ]
        else:
            assert len(contents) == len(self._translations), "Необходимы списки одинаковой длины!"
            for idx, translate in enumerate(self._translations):
                translate.content = contents[idx]

    @property
    def valid_translations(self) -> list[Extra_Word]|list:
        translations = []
        if self._translations:
            for translate in self._translations:
                translations.append(translate.validate())
        return translations

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
            self._language = Extra_Language.model_construct(
                main_language = None,
                translation_language = None,
            )
        for attr, value in kwargs.items():
            setattr(self._language, attr, value)

    @property
    def dictionary_ids(self):
        if not isinstance(self._dictionary_ids, list):
            self._dictionary_ids = []
        return self._dictionary_ids
    @dictionary_ids.setter
    def dictionary_ids(self, dictionary_ids: list[int]):
        if isinstance(dictionary_ids, list):
            self._dictionary_ids = dictionary_ids
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
    def word_translations_order(self) -> Generator[TreePathANdContentView, None, None]:
        return self._word_translations_order
    @word_translations_order.setter
    def word_translations_order(self, generator: Generator):
        if isinstance(generator, Iterator):
            self._word_translations_order = generator
    @word_translations_order.deleter
    def word_translations_order(self):
        self._word_translations_order = None

    @property
    def current_element(self) -> TreePathANdContentView|None:
        if self._current_object:
            return self._current_object
        else:
            try:
                self._current_object = next(self._word_translations_order)
                self._choice_count = len(self._current_object.translations)
                return self._current_object
            except StopIteration:
                return None
    @current_element.deleter
    def current_element(self):
        self._current_object = None

    @property
    def current_dictionary(self):
        return self._current_dictionary
    @current_dictionary.setter
    def current_dictionary(self, current_dictionary: str):
        self._current_dictionary = current_dictionary
    @current_dictionary.deleter
    def current_dictionary(self):
        self._current_dictionary = None

    @property
    def current_word(self):
        return self._current_word
    @current_word.setter
    def current_word(self, current_word: str):
        self._current_word = current_word
    @current_word.deleter
    def current_word(self):
        self._current_word = None

    @property
    def choice_count(self):
        return self._choice_count
    @choice_count.setter
    def choice_count(self, choice_count: str):
        self._choice_count = choice_count
    @choice_count.deleter
    def choice_count(self):
        self._choice_count = None

    @property
    def dialog_active(self) -> bool:
        return self._dialog_active
    @dialog_active.setter
    def dialog_active(self, dialog_active: bool):
        self._dialog_active = dialog_active

    @property
    def done_event(self) -> bool:
        return self._done_event
    @done_event.setter
    def done_event(self, done_event: bool):
        self._done_event = done_event

    def full_clear(self):
        self.__init__()

    def clear(self):
        self._old_word = None
        self._word = None
        self._translations = None
        self._note = None
        self._word_translate = None
        self._language = None
        self._dictionary_ids = None
        self._interval_ids = None
        self._word_translations_order = None
        self._current_object = None
        self._current_dictionary = None
        self._current_word = None
        self._choice_count = None
        self._dialog_active = False
