from aiograpi import Client
from aiograpi.types import DirectMessage


class InstagramClient:

    def __init__(self, cl: Client):
        self.cl = cl

    async def get_thread(self, thread_id: int):
        thread: list[DirectMessage] = await self.cl.direct_messages(thread_id=thread_id)
        thread.reverse()
        return thread

    async def send_message(self, message: str, thread_id: int):
        await self.cl.direct_send(text=message, thread_ids=[thread_id])



