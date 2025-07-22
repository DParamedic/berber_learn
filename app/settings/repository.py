from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.settings.models import Interval, Interval_List, Link_Interval_List, User_Settings
from app.settings.DTO import (
    Interval as Interval_Pydantic,
    Interval_List as Interval_List_Pydantic,
    Link_Interval_List as Link_Interval_List_Pydantic,
    User_Settings as User_Settings_Pydantic,
)

class SettingsRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create_interval_list(self, DTO: Interval_List_Pydantic) -> Interval_List:
        interval_list = Interval_List(**DTO.model_dump())
        self.session.add(interval_list)
        await self.session.commit()
        await self.session.refresh(interval_list)
        return interval_list

    async def get_interval_list_by_id(self, interval_list_id: int) -> Interval_List | None:
        result = await self.session.execute(
            select(Interval_List).where(
                Interval_List.id == interval_list_id,
            )
        )
        return result.scalar_one_or_none()

    async def get_interval_list_by_name(self, name: str) -> Interval_List | None:
        result = await self.session.execute(
            select(Interval_List).where(
                Interval_List.name == name,
            )
        )
        return result.scalar_one_or_none()
    
    async def get_all_interval_lists(self) -> list[Interval_List] | list:
        results = await self.session.execute(
            select(Interval_List)
        )
        return results.scalars().all()

    async def get_interval_lists_by_user(self, user_id: int) -> list[Interval_List] | list:
        results = await self.session.execute(
            select(Interval_List).where(
                Interval_List.id.in_(
                    select(User_Settings.interval_list_id).where(
                        User_Settings.user_id == user_id
                    )
                )
            )
        )
        return results.scalars().all()
    
    async def create_interval(self, DTO: Interval_Pydantic) -> Interval:
        interval = Interval(**DTO.model_dump())
        self.session.add(interval)
        await self.session.commit()
        await self.session.refresh(interval)
        return interval

    async def get_min_interval_by_interval_list():
        pass
    async def get_interval_by_length(self, length: int) -> Interval | None:
        result = await self.session.execute(
            select(Interval).where(
                Interval.length == length,
            )
        )
        return result.scalar_one_or_none()
    
    async def get_intervals_by_name(self, interval_list_name: str) -> list[Interval] | list:
        result = await self.session.execute(
            select(Interval).where(
                Interval.length == select(Link_Interval_List).where(
                    Link_Interval_List.interval_list_id == select(Interval_List).where(
                        Interval_List.name == interval_list_name
                    )
                )
            )
        )
        return result.scalars().all()

    async def create_link_interval_list(self, DTO: Link_Interval_List_Pydantic) -> Link_Interval_List:
        link_interval_list = Link_Interval_List(**DTO.model_dump())
        self.session.add(link_interval_list)
        await self.session.commit()
        await self.session.refresh(link_interval_list)
        return link_interval_list

    async def get_link_interval_list_by_ids(self, interval_list_id: int, interval_id: int) -> Link_Interval_List | None:
        result = await self.session.execute(
            select(Link_Interval_List).where(
                Link_Interval_List.interval_list_id == interval_list_id,
                Link_Interval_List.interval_id == interval_id,
            )
        )
        return result.scalar_one_or_none()
