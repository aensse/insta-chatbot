from dataclasses import dataclass

from fastapi import HTTPException, status

from app.infrastructure.async_queue import AsyncQueue
from app.infrastructure.db_queries import ThreadsQueries
from app.infrastructure.grok_client import GrokClient, UserInfo
from app.infrastructure.instagram_client import InstagramClient
from app.infrastructure.models import ThreadInfo, ThreadStatus
from app.infrastructure.schemas import UserMessage


@dataclass
class MessageResponderDeps:
    message: UserMessage
    db: ThreadsQueries
    ai: GrokClient
    ig: InstagramClient
    q: AsyncQueue


class Item:

    def __init__(self, deps: MessageResponderDeps, thread: ThreadInfo) -> None:
        self.deps = deps
        self.thread = thread
        self.thread_id = thread.instagram_thread_id

    async def run(self) -> None:
        thread_content = await self.deps.ig.get_thread(self.thread_id )
        grok_answer: UserInfo = await self.deps.ai.get_ai_response(thread_content)
        await self.deps.ig.send_message(grok_answer.message, self.thread_id)
        await self.deps.db.update_status(self.thread_id, grok_answer.status)


async def send_message_to_bot(deps: MessageResponderDeps):
    thread: ThreadInfo = await deps.db.get_thread_by_thread_id(deps.message.thread_id)
    if not thread:
        thread = await deps.db.add_thread(deps.message)
    if thread.status == ThreadStatus.BLOCKED:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Conversation with user already finished")

    if deps.q.is_user_in_queue(deps.message.thread_id):
        return

    item = Item(deps, thread)
    await deps.q.producer(item)

