from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.models import User
from app.auth.DTO import User as PydanticUser

class AuthRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create_user(self, DTO: PydanticUser) -> User:
        user = User(**DTO.model_dump(exclude_unset=True))
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
    
    async def get_or_create_user(self, telegram_id: int) -> User | None:
        user = await self.get_user_by_telegram_id(telegram_id)
        if user:
            return user
        else:
            user = await self.create_user(telegram_id)
            return user
    
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

        
