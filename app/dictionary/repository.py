from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dictionary.models import Dictionary, Word, Language, Translate, Note

class DictionaryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_dictionary(self, user_id: int, language_id: int) -> Dictionary:
        dictionary = Dictionary(
            user_id=user_id,
            language_id=language_id,
        )
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

    async def get_dictionaries_by_user_id(self, user_id: int) -> list[Dictionary | None]:
        result = await self.session.execute(
            select(Dictionary).where(
                Dictionary.user_id == user_id,
            )
        )
        return result.scalars().all()

    async def get_dictionaries_by_language_id(self, language_id: int) -> list[Dictionary | None]:
        result = await self.session.execute(
            select(Dictionary).where(
                Dictionary.language_id == language_id,
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

    async def create_language(self, name) -> Language:
        language = Language(
            name=name,
        )
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

    async def get_language_by_name(self, name: str) -> Language | None:
        result = await self.session.execute(
            select(Language).where(
                Language.name == name,
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

    async def create_word(self, content: str, note_id: int, dict_id: int, page_value: int, count: int) -> Language:
        word = Word(
            content=content,
            note_id=note_id,
            dict_id=dict_id,
            page_value=page_value,
            count=count,
        )
        self.session.add(word)
        await self.session.commit()
        await self.session.refresh(word)
        return word

    async def get_word_by_id(self, word_id: int) -> Language | None:
        result = await self.session.execute(
            select(Word).where(
                Word.id == word_id,
            )
        )
        return result.scalar_one_or_none()

    async def get_word_by_dict_id_and_content(self, dict_id: int, content: str) -> Language | None:
        result = await self.session.execute(
            select(Word).where(
                Word,dict_id == dict_id,
                Word.content == content,
            )
        )
        return result.scalar_one_or_none()

    async def update_word(self, word_id: int, **kwargs) -> Language:
        word = await self.get_language_by_id(word_id)
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

    async def create_translate(self, content: str, word_id: int) -> Translate:
        translate = Translate(
            content=content,
            word_id=word_id,
            )
        self.session.add(translate)
        await self.session.commit()
        await self.session.refresh(translate)
        return translate
    
    async def get_translate_by_id(self, translate_id: int) -> Translate | None:
        result = await self.session.execute(
            select(Translate).where(
                Translate.id == translate_id,
            )
        )
        return result.scalar_one_or_none()
    
    async def get_translates_by_word_id(self, word_id: int) -> list[Translate | None]:
        result = await self.session.execute(
            select(Translate).where(
                Translate.word_id == word_id,
            )
        )
        return result.scalars().all()

    async def get_translate_by_word_id_and_content(self, word_id: int, content: str) -> Translate | None:
        result = await self.session.execute(
            select(Translate).where(
                Translate.word_id == word_id,
                Translate.content == content,
            )
        )
        return result.scalar_one_or_none()
    
    async def update_translate(self, translate_id: int, **kwargs) -> Translate | None:
        translate = await self.get_translate_by_id(translate_id)
        if translate:
            for key, value in kwargs.items():
                setattr(translate, key, value)
            await self.session.refresh(translate)
            return translate
        return translate
    
    async def delete_translate(self, translate_id: int) -> bool:
        translate = await self.get_translate_by_id(translate_id)
        if translate:
            await self.session.delete(translate)
            return True
        return False
    
    async def create_note(self, content: str) -> Note:
        note = Note(content=content)
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
