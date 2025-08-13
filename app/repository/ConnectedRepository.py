from app.repository import Decorators as ds
from app.repository.Repository import Repository
from app.models import *
from app.DTO import (
    Valid_Dictionary,
    Valid_Language,
    Valid_Word,
    Valid_Word_Translate,
    Valid_User,
)

class ConnectedRepository(Repository):
    """Репозиторий с выполненным соединением"""
    @classmethod
    @ds.connect
    async def get_or_create_user(
        cls,
        DTO: Valid_User,
    ) -> User:
        return cls._get_or_create_user

    @classmethod
    @ds.connect
    async def create_dictionary(
        cls,
        DTO: Valid_Dictionary,
    ) -> Dictionary:
        return cls._create_dictionary

    @classmethod
    @ds.connect
    async def get_dictionary(
        cls,
        *,
        id: int = None,
        user_id: int = None,
        language_id: int = None,
        interval_list_id: int = None,
    ) -> Dictionary|None:
        return cls._get_dictionary

    @classmethod
    @ds.connect
    async def get_dictionaries(
        cls,
        user_id: int,
    ) -> list[Dictionary]|list:
        return cls._get_dictionaries

    @classmethod
    @ds.connect
    async def get_dict_info(
        cls,
        dictionaries: list[Dictionary],
    ):
        return cls._get_dict_info

    @classmethod
    @ds.connect
    async def get_or_create_language(
        cls,
        DTO: Valid_Language,
    ) -> Language:
        return cls._get_or_create_language

    @classmethod
    @ds.connect
    async def get_or_create_word(
        cls,
        DTO: Valid_Word,
    ) -> Word:
        return cls._get_or_create_word

    @classmethod
    @ds.connect
    async def get_or_create_translations(
        cls,
        DTOs: list[Valid_Word],
    ) -> list[Word]:
        return cls._get_or_create_translations

    @classmethod
    @ds.connect
    async def get_or_create_note(
        cls,
        DTO: Valid_Word,
    ) -> Note:
        return cls._get_or_create_note

    @classmethod
    @ds.connect
    async def create_word_translations(
        cls,
        DTO: Valid_Word_Translate,
    ) -> bool:
        """Возвращает True, если создана хоть одна запись"""
        return cls._create_word_translations

    @classmethod
    @ds.connect
    async def get_word_translations_inf(
        cls,
        word_content: str,
        dictionary_id: int,
    ) -> dict[str, str|list[str]]:
        return cls._get_word_translations_inf

    @classmethod
    @ds.connect
    async def update_word_translations_count(
        cls,
        user_id: int,
    ) -> list[Word_Translate]|list:
        return cls._update_word_translations_count

    @classmethod
    @ds.connect
    async def update_word_translate_interval_up(
        cls,
        dictionary_id: int,
        word_id: int,
        translate_id: int,
        interval_list_id: int,
        count: int,
    ) -> None:
        return cls._update_word_translate_interval_up

    @classmethod
    @ds.connect
    async def update_word_translate_interval_down(
        cls,
        dictionary_id: int,
        word_id: int,
        translate_id: int,
        interval_list_id: int,
    ) -> None:
        return cls._update_word_translate_interval_down

    @classmethod
    @ds.connect
    async def delete_word_translations(
        cls,
        dictionary_id: int,
        word_content: str,
    ) -> None:
        return cls._delete_word_translations

    @classmethod
    @ds.connect
    async def get_interval_lists_by_user(
        cls,
        user_id: int
    ) -> list[Interval_List] | list:
        return cls._get_interval_lists_by_user

    @classmethod
    @ds.connect
    async def get_classic_interval(
        cls,
        interval_list_name: str,
        interval_lengths: list[int],
    ) -> None:
        return cls._get_classic_interval
