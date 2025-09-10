from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload, aliased

from app.repository import Decorators as ds
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
    Valid_User_Settings,
)

class Repository:
    def __init__(self, session):
        self.session: AsyncSession = session

    @ds.create_model(User)
    async def _create_user(
        self,
        DTO: Valid_User,
    ) -> User:
        ...
    
    @ds.create_model(Dictionary)
    async def _create_dictionary(
        self,
        DTO: Valid_Dictionary,
    ) -> Dictionary:
        ...

    @ds.create_model(Language)
    async def _create_language(
        self,
        DTO: Valid_Language,
    ) -> Language:
        ...

    @ds.create_model(Word)
    async def _create_word(
        self,
        DTO: Valid_Word,
    ) -> Word:
        ...

    @ds.create_model(Word_Translate)
    async def _create_word_translate(
        self,
        DTO: Valid_Word_Translate,
    ) -> Word_Translate:
        ...

    @ds.create_model(Note)
    async def _create_note(
        self,
        DTO: Valid_Word,
    ) -> Note:
        ...

    @ds.create_model(Interval)
    async def _create_interval(
        self,
        DTO: Valid_Interval,
    ) -> Interval:
        ...

    @ds.create_model(Interval_List)
    async def _create_interval_list(
        self,
        DTO: Valid_Interval_List,
    ) -> Interval_List:
        ...

    @ds.create_model(Link_Interval_List)
    async def _create_link_interval_list(
        self,
        DTO: Valid_Link_Interval_List,
    ) -> Link_Interval_List:
        ...

    @ds.create_model(User_Settings)
    async def _create_user_settings(
        self,
        DTO: Valid_User_Settings,
    ) -> User_Settings:
        ...

    @ds.get_model(User)
    async def _get_user(
        self,
        *,
        id: int = None,
        telegram_id: str = None,
    ) -> User|None:
        ...

    @ds.get_model(Dictionary)
    async def _get_dictionary(
        self,
        *,
        id: int = None,
        user_id: int = None,
        language_id: int = None,
        interval_list_id: int = None,
    ) -> Dictionary|None:
        ...

    @ds.get_model(Language)
    async def _get_language(
        self,
        *,
        id: int = None,
        main_language: str = None,
        translation_language: str = None,
    ) -> Language|None:
        ...

    @ds.get_model(Word)
    async def _get_word(
        self,
        *,
        id: int = None,
        content: str = None,
    ) -> Word|None:
        ...

    @ds.get_model(Note)
    async def _get_note(
        self,
        *,
        id: int = None,
        content: str = None,
    ) -> Note|None:
        ...

    @ds.get_model(Word_Translate)
    async def _get_word_translate(
        self,
        *,
        dictionary_id: int = None,
        word_id: int = None,
        translate_id: int = None,
        note: int = None,
        interval_id: int = None,
        count: int = None,
    ) -> Word_Translate|None:
        ...

    @ds.get_model(Interval)
    async def _get_interval(
        self,
        *,
        id: int = None,
        length: str = None,
    ) -> Interval|None:
        ...

    @ds.get_model(Interval_List)
    async def _get_interval_list(
        self,
        *,
        id: int = None,
        name: str = None,
    ) -> Interval_List|None:
        ...

    @ds.get_model(Link_Interval_List)
    async def _get_link_interval_list(
        self,
        *,
        interval_id: int = None,
        interval_list_id: int = None,
    ) -> Link_Interval_List|None:
        ...

    @ds.get_model(User_Settings)
    async def _get_user_settings(
        self,
        *,
        user_id: int = None,
        interval_list_id: int = None,
    ) -> User_Settings|None:
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

    async def _get_or_create_translations(self, DTOs: list[Valid_Word]):
        translations = []
        for DTO in DTOs:
            translate = await self._get_word(**DTO.model_dump())
            if not translate:
                translate = await self._create_word(DTO)
            translations.append(translate)
        return translations

    async def _get_or_create_note(
        self,
        DTO: Valid_Word,
    ) -> Note:
        result = await self._get_note(**DTO.model_dump())
        if not result:
            result = await self._create_note(DTO)
        return result

    async def _create_word_translations(
        self,
        DTO: Valid_Word_Translate
    ) -> bool:
        is_created = False
        for translate_id in DTO.translate_ids:
            DTO_dump = DTO.model_dump(exclude={"translate_ids"})
            DTO_dump.update({"translate_id": translate_id})
            word_translate = await self._get_word_translate(**DTO_dump)
            if not word_translate:
                word_translate = Word_Translate(**DTO_dump)
                self.session.add(word_translate)
                await self.session.commit()
                is_created = True
        return is_created

    async def _get_word_translations_inf(
        self,
        word_content: str,
        dictionary_id: int,
    ) -> dict[str, list[str|int]|None]:
        word_translations = await self.session.execute(
            select(Word_Translate).options(
                selectinload(Word_Translate.interval),
                selectinload(Word_Translate.translate),
            ).where(
                Word_Translate.dictionary_id == dictionary_id,
                Word_Translate.word_id == (
                    select(Word.id)
                    .where(Word.content == word_content)
                    .scalar_subquery()
                )
            )
        )
        word_translations = word_translations.scalars().all()
        if not word_translations:
            return None
        note = await self.session.execute(
            select(Note).where(
                Note.id.in_(
                    (w_t.note_id for w_t in word_translations)
                )
            )
        )
        note = note.scalar_one_or_none()
        return dict(
            translations=[w_t.translate.content for w_t in word_translations],
            note=note.content if note else None,
            interval=[w_t.interval.length for w_t in word_translations],
            count=[w_t.count for w_t in word_translations]
        )
    async def _update_word_translations_count(
        self,
        user_id: int,
    ) -> list[Word_Translate]|list:
        word_translations_table = (await self.session.execute(
            select(Word_Translate)
            .options(
                selectinload(Word_Translate.dictionary)
                .selectinload(Dictionary.language),
                selectinload(Word_Translate.word),
                selectinload(Word_Translate.translate),
                selectinload(Word_Translate.interval),
            )
            .join(Dictionary, Dictionary.id == Word_Translate.dictionary_id)
            .join(User, User.id == Dictionary.user_id)
            .where(User.id == user_id)
            .order_by(Word_Translate.dictionary_id, Word_Translate.word_id)
        )).scalars().all()

        out_word_translations = []
        for word_translate in word_translations_table:
            if word_translate.count < word_translate.interval.length:
                word_translate.count += 1
            else:
                out_word_translations.append(word_translate)
        await self.session.commit()
        return out_word_translations

    async def _update_word_translate_interval_up(
        self,
        dictionary_id: int,
        word_id: int,
        translate_id: int,
        interval_list_id: int,
        count: int,
    ) -> None:
        word_translate = await self._get_word_translate(
            dictionary_id=dictionary_id,
            word_id=word_id,
            translate_id=translate_id,
        )
        word_translate.interval_id = await self.session.scalar(
            select(Interval.id).where(
                Interval.length == (
                    select(func.min(Interval.length))
                    .join(
                        Link_Interval_List,
                        Link_Interval_List.interval_id == Interval.id,
                    )
                    .join(
                        Interval_List,
                        Interval_List.id == Link_Interval_List.interval_list_id,
                    )
                    .where(
                        Interval_List.id == interval_list_id,
                        Interval.length > count,
                    )
                    .scalar_subquery()
                )
            )
        )
        word_translate.count = 0
        await self.session.commit()
        await self.session.refresh(word_translate)
        return None

    async def _update_word_translate_interval_down(
        self,
        dictionary_id: int,
        word_id: int,
        translate_id: int,
        interval_list_id: int,
    ) -> None:
        word_translate = await self._get_word_translate(
            dictionary_id=dictionary_id,
            word_id=word_id,
            translate_id=translate_id,
        )
        word_translate.interval_id = await self.session.scalar(
            select(Interval.id).where(
                Interval.length == (
                    select(func.min(Interval.length))
                    .join(
                        Link_Interval_List,
                        Link_Interval_List.interval_id == Interval.id,
                    )
                    .join(
                        Interval_List,
                        Interval_List.id == Link_Interval_List.interval_list_id,
                    )
                    .where(
                        Interval_List.id == interval_list_id
                    )
                    .scalar_subquery()
                )
            )
        )
        word_translate.count = 0
        await self.session.commit()
        return None

    async def _delete_word_translations(
        self,
        dictionary_id: int,
        word_content: str,
    ) -> None:
        word_translations = await self.session.execute(
            select(Word_Translate).where(
                Word_Translate.dictionary_id == dictionary_id,
                Word_Translate.word_id.in_(
                    select(Word.id).where(
                        Word.content == word_content,
                    )
                )
            )
        )
        word_translations = word_translations.scalars().all()
        for word_translate in word_translations:
            await self.session.delete(word_translate)
        await self.session.commit()
        return None

    async def _get_interval_lists_by_user(
        self,
        user_id: int
    ) -> list[Interval_List] | list:
        results = await self.session.execute(
            select(Interval_List)
            .where(
                Interval_List.id == (
                    select(User_Settings.interval_list_id)
                    .where(User_Settings.user_id == user_id)
                )
            )
        )
        return results.scalars().all()

    async def _create_classic_interval(
        self,
        user_id: int,
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
        user_settings = await self._get_user_settings(
            user_id=user_id, 
            interval_list_id=interval_list.id
        )
        if not user_settings:
            await self._create_user_settings(
                Valid_User_Settings(
                    user_id=user_id,
                    interval_list_id=interval_list.id
                )
            )
        return None
