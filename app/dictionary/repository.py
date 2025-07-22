from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.dictionary.DTO import (
    Dictionary as Dictionary_Pydantic,
    Language as Language_Pydantic,
    Word as Word_Pydantic,
    Note as Note_Pydantic,
    Word_Translate as Word_Translate_Pydantic,
    )
from app.dictionary.models import Dictionary, Word, Language, Note, Word_Translate
from app.settings.models import Interval_List, Interval


class DictionaryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_dictionary(self, DTO: Dictionary_Pydantic) -> Dictionary:
        dictionary = Dictionary(**DTO.model_dump())
        self.session.add(dictionary)
        await self.session.commit()
        await self.session.refresh(dictionary)
        return dictionary

    async def get_dictionary_by_id(self, dictionary_id: int) -> Dictionary | None:
        result = await self.session.execute(
            select(Dictionary).where(
                Dictionary.id == dictionary_id,
            )
        )
        return result.scalar_one_or_none()

    async def get_dictionary_by_user_id_language_id(
        self,
        user_id: int,
        language_id: int,
        ) -> Dictionary | None:
        result = await self.session.execute(
            select(Dictionary).where(
                Dictionary.user_id == user_id,
                Dictionary.language_id == language_id,
            )
        )
        return result.scalar_one_or_none()

    async def get_dictionaries_by_user_id(
        self, user_id: int
    ) -> list[Dictionary]|list:
        result = await self.session.execute(
            select(Dictionary).where(
                Dictionary.user_id == user_id,
            )
        )
        return result.scalars().all()

    async def update_dictionary(self, dictionary_id: int, **kwargs) -> Dictionary:
        dictionary = await self.get_user_by_id(dictionary_id)
        if dictionary:
            for key, value in kwargs:
                setattr(dictionary, key, value)
            await self.session.commit()
            await self.session.refresh(dictionary)
        return dictionary

    async def delete_dictionary(self, dictionary_id) -> bool:
        dictionary = self.get_dictionary_by_id(dictionary_id)
        if dictionary:
            await self.session.delete(dictionary)
            await self.session.commit()
            return True
        return False

    async def create_language(self, DTO: Language_Pydantic) -> Language:
        language = Language(**DTO.model_dump())
        self.session.add(language)
        await self.session.commit()
        await self.session.refresh(language)
        return language

    async def get_language_by_id(self, language_id: int) -> Language | None:
        result = await self.session.execute(
            select(Language).where(
                Language.id == language_id,
            )
        )
        return result.scalar_one_or_none()

    async def get_language_by_languages(
        self,
        main_language: str,
        translation_language: str,
        ) -> Language | None:
        result = await self.session.execute(
            select(Language).where(
                Language.main_language == main_language,
                Language.translation_language == translation_language,
            )
        )
        return result.scalar_one_or_none()

    async def update_language(self, language_id: int, **kwargs) -> Language:
        language = await self.get_language_by_id(language_id)
        if language:
            for key, value in kwargs:
                setattr(language, key, value)
            await self.session.commit()
            await self.session.refresh(language)
        return language

    async def delete_language(self, language_id: int) -> bool:
        language = await self.get_language_by_id(language_id)
        if language:
            await self.session.delete(language)
            await self.session.commit()
            return True
        return False

    async def create_word(self, DTO: Word_Pydantic) -> Word:
        word = Word(**DTO.model_dump())
        self.session.add(word)
        await self.session.commit()
        await self.session.refresh(word)
        return word

    async def get_word_by_id(self, word_id: int) -> Word | None:
        result = await self.session.execute(
            select(Word).where(
                Word.id == word_id,
            )
        )
        return result.scalar_one_or_none()

    async def get_word_by_content(self, content: str) -> Word | None:
        result = await self.session.execute(
            select(Word).where(
                Word.content == content,
            )
        )
        return result.scalar_one_or_none()

    async def update_word(self, word_id: int, **kwargs) -> Word:
        word = await self.get_word_by_id(word_id)
        if word:
            for key, value in kwargs:
                setattr(word, key, value)
            await self.session.commit()
            await self.session.refresh(word)
        return word

    async def delete_word(self, word_id: int) -> bool:
        word = await self.get_word_by_id(word_id)
        if word:
            await self.session.delete(word)
            await self.session.commit()
            return True
        return False

    async def create_note(self, DTO: Note_Pydantic) -> Note:
        note = Note(**DTO.model_dump())
        self.session.add(note)
        await self.session.commit()
        await self.session.refresh(note)
        return note

    async def get_note_by_id(self, note_id: int) -> Note | None:
        result = await self.session.execute(
            select(Note).where(
                Note.id == note_id,
            )
        )
        return result.scalar_one_or_none()

    async def get_note_by_content(self, content: str) -> Note | None:
        result = await self.session.execute(
            select(Note).where(
                Note.content == content,
            )
        )
        return result.scalar_one_or_none()
    async def update_note(self, note_id: int, **kwargs) -> Note | None:
        note = await self.get_note_by_id(note_id)
        if note:
            for key, value in kwargs:
                setattr(note, key, value)
            await self.session.commit()
            await self.session.refresh(note)
            return note
        return note

    async def delete_note(self, note_id: int) -> bool:
        note = await self.get_note_by_id(note_id)
        if note:
            await self.session.delete(note)
            return True
        return False

    async def create_word_translates(self, DTO: Word_Translate_Pydantic) -> list[Word_Translate] | list:
        """Создание n Word_Translate (n = len(DTO.translate_ids))"""
        word_translate_list = []
        for translate_id in DTO.translate_ids:
            word_translate_ = DTO.model_dump(exclude={"translate_ids"})
            word_translate_.update({"translate_id": translate_id})
            word_translate = Word_Translate(
                **word_translate_,
            )
            self.session.add(word_translate)
            await self.session.commit()
            await self.session.refresh(word_translate)
            word_translate_list.append(word_translate)
        return word_translate_list
    
    async def get_word_and_translates(
        self,
        word_content: str,
        dictionary_id: int,
    ) -> dict[str, str|list[str]]:
        word = await self.get_word_by_content(word_content)
        if not word:
            return None
        translates = await self.session.execute(
            select(Word).where(
                Word.id.in_(
                    select(Word_Translate.translate_id).where(
                        Word_Translate.word_id == word.id,
                        Word_Translate.dictionary_id == dictionary_id,
                        )
                    )
                )
            )
        note = await self.session.execute(
            select(Note).where(
                Note.id.in_(
                    select(Word_Translate.note_id).where(
                        Word_Translate.word_id == word.id
                    )
                )
            )
        )
        interval_list = await self.session.execute(
            select(Interval).where(
                Interval.id.in_(select(Word_Translate.interval_id).where(
                    Word_Translate.word_id == word.id
                    )
                )
            )
        )
        count = await self.session.execute(
            select(Word_Translate.count).where(
                Word_Translate.word_id == word.id
            )
        )
        translates = translates.scalars().all()
        note = note.scalar()
        interval_list = interval_list.scalar()
        count = count.scalar()
        return dict(
            word=word.content,
            translates = [translate.content for translate in translates],
            note = note.content if note else None,
            interval_list=interval_list.length,
            count=count,
            )
        
    async def update_word_translates(self, DTO: Word_Translate_Pydantic):
        word_translate_list = []
        for translate_id in DTO.translate_ids:
            word_translate_ = DTO.model_dump(exclude={"translate_ids"})
            word_translate_.update({"translate_id": translate_id})
            word_translate = await self.session.execute(
                select(Word_Translate).where(
                    Word_Translate.dictionary_id == word_translate_["dictionary_id"],
                    Word_Translate.word_id == word_translate_["word_id"],
                    Word_Translate.translate_id == word_translate_["translate_id"],
                )
            )
            word_translate = word_translate.scalar_one_or_none()
            word_translate = Word_Translate(
                **word_translate_,
            )
            self.session.add(word_translate)
            await self.session.commit()
            await self.session.refresh(word_translate)
            word_translate_list.append(word_translate)
        return word_translate_list
        
    async def delete_word_translates_by_word(
        self,
        dictionary_id: int,
        word_content: str,
    ):
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
