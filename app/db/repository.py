from functools import wraps

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User, Dictionary, Word, Language
from app.database import async_session_maker

class Repository:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.connect = None
        
    def connection(method):
        @wraps(method)
        async def _wrapper(self, *args, **kwargs):
            async with async_session_maker() as session:
                try:
                    self.connect = session
                    return await method(self, *args, **kwargs)
                except Exception as err:
                    await session.rollback()
                    print(f'Error: {err}')
                    raise err
        return _wrapper
    
    
    async def create_user(self, telegram_id: int, name: str | None) -> User:
        user = User(
            telegram_id=telegram_id,
            name=name,
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user
    
    async def get_user_by_id(self, user_id: int) -> User | None:
        result = await self.session.execute(
            select(User).where(
                User.id == user_id,
            )
        )
        return result.scalar_one_or_none()
    
    async def get_user_by_telegram_id(self, telegram_id: int) -> User | None:
        result = await self.session.execute(
            select(User).where(
                User.telegram_id == telegram_id,
            )
        )
        return result.scalar_one_or_none()
    
    async def update_user(self, user_id: int, **kwargs) -> User | None:
        user = await self.get_user_by_id(user_id)
        if user:
            for key, value in kwargs:
                setattr(User, key, value)
            await self.session.commit()
            await self.session.refresh(user)
        return user
    
    async def delete_user(self, user_id: int) -> bool:
        user = self.get_user_by_id(user_id)
        if user:
            await self.session.delete(user)
            await self.session.commit()
            return True
        return False
    
    async def create_dictionary(self, user_id: int) -> Dictionary:
        dictionary = Dictionary(
            user_id=user_id,
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
    
    async def update_dictionary(self, dictionary_id: int, **kwargs) -> Dictionary:
        dictionary = await self.get_user_by_id(dictionary_id)
        if dictionary:
            for key, value in kwargs:
                setattr(Dictionary, key, value)
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
                setattr(Language, key, value)
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
    
    async def create_word(self, content: str, dict_id: int, page_value: int, count: int) -> Language:
        word = Word(
            content=content,
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
                setattr(Word, key, value)
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

