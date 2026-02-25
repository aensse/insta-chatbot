import asyncio
from typing import Protocol


class Item(Protocol):

    thread_id = ...

    async def run(self) -> None: ...


class AsyncQueue:

    def __init__(self, q: asyncio.Queue) -> None:
        self.q = q
        self.cache: set[str] = set()

    async def producer(self, item: Item) -> None:
        self.cache.add(item.thread_id)
        await self.q.put(item)

    async def consumer(self) -> None:
        while True:
            item: Item = await self.q.get()
            await item.run()
            self.cache.remove(item.thread_id)
            self.q.task_done()

    def is_user_in_queue(self, thread_id: str) -> bool:
        return thread_id in self.cache
