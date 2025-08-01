from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.repository.Repo import Repo
from app.models import *
from app.DTO import (
    Valid_Dictionary,
    Valid_Language,
    Valid_Word,
    Valid_Word_Translate,
    Valid_User,
    Valid_Interval,
    Valid_Interval_List,
    Valid_Link_Interval_List,
)

class Repository:
    def __init__(self, session):
        self.session: AsyncSession = session

    @classmethod
    @Repo.connect
    async def get_or_create_user(
        cls,
        DTO: Valid_User,
    ) -> User:
        return cls._get_or_create_user

    @classmethod
    @Repo.connect
    async def create_dictionary(
        cls,
        DTO: Valid_Dictionary,
    ) -> Dictionary:
        return cls._create_dictionary

    @classmethod
    @Repo.connect
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
    @Repo.connect
    async def get_dictionaries(
        cls,
        user_id: int,
    ) -> list[Dictionary]|list:
        return cls._get_dictionaries

    @classmethod
    @Repo.connect
    async def get_dict_info(
        cls,
        dictionaries: list[Dictionary],
    ):
        return cls._get_dict_info

    @classmethod
    @Repo.connect
    async def get_or_create_language(
        cls,
        DTO: Valid_Language,
    ) -> Language:
        return cls._get_or_create_language

    @classmethod
    @Repo.connect
    async def get_or_create_word(
        cls,
        DTO: Valid_Word,
    ) -> Word:
        return cls._get_or_create_word

    @classmethod
    @Repo.connect
    async def get_or_create_translates(
        cls,
        DTOs: list[Valid_Word],
    ) -> list[Word]:
        return cls._get_or_create_translates

    @classmethod
    @Repo.connect
    async def get_or_create_note(
        cls,
        DTO: Valid_Word,
    ) -> Note:
        return cls._get_or_create_note

    @classmethod
    @Repo.connect
    async def create_word_translates(
        cls,
        DTO: Valid_Word_Translate,
    ) -> bool:
        """Возвращает True, если создана хоть одна запись"""
        return cls._create_word_translates

    @classmethod
    @Repo.connect
    async def get_word_translates_inf(
        cls,
        word_content: str,
        dictionary_id: int,
    ) -> dict[str, str|list[str]]:
        return cls._get_word_translates_inf

    @classmethod
    @Repo.connect
    async def delete_word_translates(
        cls,
        dictionary_id: int,
        word_content: str,
    ) -> None:
        return cls._delete_word_translates

    @classmethod
    @Repo.connect
    async def get_interval_lists_by_user(
        cls,
        user_id: int
    ) -> list[Interval_List] | list:
        return cls._get_interval_lists_by_user

    @classmethod
    @Repo.connect
    async def get_classic_interval(
        cls,
        interval_list_name: str,
        interval_lengths: list[int],
    ) -> None:
        return cls._get_classic_interval

    @Repo.create_model(User)
    async def _create_user(
        self,
        DTO: Valid_User,
    ) -> User:
        ...
    
    @Repo.create_model(Dictionary)
    async def _create_dictionary(
        self,
        DTO: Valid_Dictionary,
    ) -> Dictionary:
        ...

    @Repo.create_model(Language)
    async def _create_language(
        self,
        DTO: Valid_Language,
    ) -> Language:
        ...

    @Repo.create_model(Word)
    async def _create_word(
        self,
        DTO: Valid_Word,
    ) -> Word:
        ...

    @Repo.create_model(Word_Translate)
    async def _create_word_translate(
        self,
        DTO: Valid_Word_Translate,
    ) -> Word_Translate:
        ...

    @Repo.create_model(Note)
    async def _create_note(
        self,
        DTO: Valid_Word,
    ) -> Note:
        ...

    @Repo.create_model(Interval)
    async def _create_interval(
        self,
        DTO: Valid_Interval,
    ) -> Interval:
        ...

    @Repo.create_model(Interval_List)
    async def _create_interval_list(
        self,
        DTO: Valid_Interval_List,
    ) -> Interval_List:
        ...

    @Repo.create_model(Link_Interval_List)
    async def _create_link_interval_list(
        self,
        DTO: Valid_Link_Interval_List,
    ) -> Link_Interval_List:
        ...

    @Repo.get_model(User)
    async def _get_user(
        self,
        *,
        id: int = None,
        telegram_id: str = None,
    ) -> User|None:
        ...

    @Repo.get_model(Dictionary)
    async def _get_dictionary(
        self,
        *,
        id: int = None,
        user_id: int = None,
        language_id: int = None,
        interval_list_id: int = None,
    ) -> Dictionary|None:
        ...

    @Repo.get_model(Language)
    async def _get_language(
        self,
        *,
        id: int = None,
        main_language: str = None,
        translation_language: str = None,
    ) -> Language|None:
        ...

    @Repo.get_model(Word)
    async def _get_word(
        self,
        *,
        id: int = None,
        content: str = None,
    ) -> Word|None:
        ...

    @Repo.get_model(Note)
    async def _get_note(
        self,
        *,
        id: int = None,
        content: str = None,
    ) -> Note|None:
        ...

    @Repo.get_model(Word_Translate)
    async def _get_word_translate(
        self,
        *,
        dict_id: int = None,
        word_id: int = None,
        translate_id: int = None,
        note: int = None,
        interval_id: int = None,
        count: int = None,
    ) -> Word_Translate|None:
        ...

    @Repo.get_model(Interval)
    async def _get_interval(
        self,
        *,
        id: int = None,
        length: str = None,
    ) -> Interval|None:
        ...

    @Repo.get_model(Interval_List)
    async def _get_interval_list(
        self,
        *,
        id: int = None,
        name: str = None,
    ) -> Interval_List|None:
        ...

    @Repo.get_model(Link_Interval_List)
    async def _get_link_interval_list(
        self,
        *,
        interval_id: int = None,
        interval_list_id: int = None,
    ) -> Link_Interval_List|None:
        ...

    async def _get_or_create_user(
        self,
        DTO: Valid_User,
    ) -> User:
        result = await self._get_user(**DTO.model_dump())
        if not result:
            result = await self._create_user(DTO)
        return result

    async def _get_dictionaries(
        self,
        user_id: int,
    ) -> list[Dictionary]|list:
        result = await self.session.execute(
            select(Dictionary).where(
                Dictionary.user_id == user_id,
            )
        )
        return result.scalars().all()

    async def _get_dict_info(
        self,
        dictionaries: list[Dictionary],
    ) -> list[tuple[int, str, str, str]]|list:
        info = []
        for idx, dictionary in enumerate(dictionaries):
            language = await self._get_language(id=dictionary.language_id)
            interval_list = await self._get_interval_list(
                id=dictionary.interval_list_id)
            info.append(
                (
                    idx,
                    language.main_language,
                    language.translation_language,
                    interval_list.name,
                )
            )
        return info
    async def _get_or_create_language(
        self,
        DTO: Valid_Language,
    ) -> Language:
        result = await self._get_language(**DTO.model_dump())
        if not result:
            result = await self._create_language(DTO)
        return result

    async def _get_or_create_word(
        self,
        DTO: Valid_Word,
    ) -> Word:
        result = await self._get_word(**DTO.model_dump())
        if not result:
            result = await self._create_word(DTO)
        return result

    async def _get_or_create_translates(self, DTOs: list[Valid_Word]):
        translates = []
        for DTO in DTOs:
            translate = await self._get_word(**DTO.model_dump())
            if not translate:
                translate = await self._create_word(DTO)
            translates.append(translate)
        return translates

    async def _get_or_create_note(
        self,
        DTO: Valid_Word,
    ) -> Note:
        result = await self._get_note(**DTO.model_dump())
        if not result:
            result = await self._create_note(DTO)
        return result

    async def _create_word_translates(
        self,
        DTO: Valid_Word_Translate
    ) -> bool:
        translates = False
        for translate_id in DTO.translate_ids:
            DTO_dump = DTO.model_dump(exclude={"translate_ids"})
            DTO_dump.update({"translate_id": translate_id})
            word_translate = await self._get_word_translate(**DTO_dump)
            if not word_translate:
                word_translate = Word_Translate(**DTO_dump)
                self.session.add(word_translate)
                await self.session.commit()
                translates = True
        return translates

    async def _get_word_translates_inf(
        self,
        word_content: str,
        dictionary_id: int,
    ) -> dict[str, list[str|int]|None]:
        word_translates = await self.session.execute(
            select(Word_Translate).options(
                selectinload(Word_Translate.interval)
            ).where(
                Word_Translate.dictionary_id == dictionary_id,
                Word_Translate.word_id == (
                    select(Word.id)
                    .where(Word.content == word_content)
                    .scalar_subquery()
                )
            )
        )
        word_translates = word_translates.scalars().all()

        if not word_translates:
            return None
        translates = await self.session.execute(
            select(Word).where(
                Word.id.in_(
                    (w_t.translate_id for w_t in word_translates)
                )
            )
        )
        translates = translates.scalars().all()
        note = await self.session.execute(
            select(Note).where(
                Note.id.in_(
                    (w_t.note_id for w_t in word_translates)
                )
            )
        )
        note = note.scalar_one_or_none()
        return dict(
            translates=[translate.content for translate in translates],
            note=note.content if note else None,
            interval=[w_t.interval.length for w_t in word_translates],
            count=[w_t.count for w_t in word_translates]
        )
    async def _delete_word_translates(
        self,
        dictionary_id: int,
        word_content: str,
    ) -> None:
        word_translates = await self.session.execute(
            select(Word_Translate).where(
                Word_Translate.dictionary_id == dictionary_id,
                Word_Translate.word_id.in_(
                    select(Word.id).where(
                        Word.content == word_content,
                    )
                )
            )
        )
        word_translates = word_translates.scalars().all()
        for word_translate in word_translates:
            await self.session.delete(word_translate)
        await self.session.commit()
        return None

    async def _get_interval_lists_by_user(
        self,
        user_id: int
    ) -> list[Interval_List] | list:
        results = await self.session.execute(
            select(Interval_List).where(
                Interval_List.id.in_(
                    select(Dictionary.interval_list_id).where(
                        Dictionary.user_id == user_id
                    )
                )
            )
        )
        return results.scalars().all()

    async def _get_classic_interval(
        self,
        interval_list_name: str,
        interval_lengths: list[int],
    ) -> None:
        interval_list = await self._get_interval_list(
            name=interval_list_name,
        )
        if not interval_list:
            interval_list = await self._create_interval_list(
                Valid_Interval_List(name=interval_list_name),
            )
        for length in interval_lengths:
            interval = await self._get_interval(length=length)
            if not interval:
                interval = await self._create_interval(
                    Valid_Interval(length=length),
                )
            link_interval_list = await self._get_link_interval_list(
                interval_id=interval.id,
                interval_list_id=interval_list.id,
            )
            if not link_interval_list:
                link_interval_list = await self._create_link_interval_list(
                    Valid_Link_Interval_List(
                        interval_id=interval.id,
                        interval_list_id=interval_list.id,
                    ),
                )
        return None
