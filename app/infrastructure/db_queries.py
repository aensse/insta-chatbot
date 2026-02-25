from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure import models
from app.infrastructure.schemas import UserMessage


class ThreadsQueries:

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_thread_by_thread_id(self, thread_id: str) -> models.ThreadInfo | None:
        stmt = select(models.ThreadInfo).where(models.ThreadInfo.instagram_thread_id == thread_id)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def add_thread(self, message: UserMessage) -> None:
        thread = models.ThreadInfo(
            instagram_user_id=message.user_id, instagram_thread_id=message.thread_id, name=message.user
        )
        self.db.add(thread)
        await self.db.commit()
        await self.db.refresh(thread)
        return thread

    async def update_status(self, thread_id: str, new_status: models.ThreadStatus) -> None:
        thread: models.ThreadInfo = await self.get_thread_by_thread_id(thread_id)
        thread.status = new_status
        await self.db.commit()
        await self.db.refresh(thread)




