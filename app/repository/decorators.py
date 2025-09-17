from typing import Coroutine, Callable

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import async_session_maker, Base

def connect(method: Coroutine):
    """Необходимо, чтоб декорируемый метод был classmethod и возвращал unbound method c выполняемой логикой"""
    async def wrapper(cls, *args, **kwargs):
        async with async_session_maker() as session:
            try:
                call_method = await method(cls, *args, **kwargs)
                repository = cls(session)
                return await call_method(repository, *args, **kwargs)
            except Exception as Error:
                print(f"Error: {Error}")
                await session.rollback()
                raise Error
    return wrapper

def create_model(model: Base):
    def _create_model(method: Callable):
        async def wrapper(self, DTO: BaseModel):
            row = model(**DTO.model_dump())
            self.session.add(row)
            await self.session.commit()
            await self.session.refresh(row)
            return row
        return wrapper
    return _create_model

def get_model(model: Base):
    def _get_model_by_id(method: Callable):
        async def wrapper(self, **kwargs):
            row = await self.session.execute(
                select(model).where(
                    *tuple(
                        getattr(model, attr) == value
                        for attr, value
                        in kwargs.items()
                        if value
                    )
                )
            )
            return row.scalar_one_or_none()
        return wrapper
    return _get_model_by_id

def update_model_by_id(model: Base) -> Callable:
    def _update_model_by_id(method: Callable) -> Callable:
        async def wrapper(self, id: int, **kwargs) -> Base:
            row = await self.session.execute(
                select(model).where(
                    model.id == id
                )
            )
            if row:
                for attr, value in kwargs.items():
                    setattr(row, attr, value)
                await self.session.commit()
                await self.session.refresh(row)
            return row
        return wrapper
    return _update_model_by_id

def delete_model_by_id(model: Base):
    def _delete_model_by_id(method: Callable):
        async def wrapper(self, id: int):
            row = await self.session.execute(
                select(model).where(
                    model.id == id
                )
            )
            if row:
                self.session.delete(row)
                self.session.commit()
                return True
            return False
        return wrapper
    return _delete_model_by_id
