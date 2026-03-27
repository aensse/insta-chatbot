import asyncio

from app.domain.errors import InvalidStatus
from app.domain.models import InstagramMessage, LLMResponse
from app.ports.db_port import UsersDBPort
from app.ports.instagram_port import InstagramPort
from app.ports.llm_port import LLMPort

USERS_WAITING_FOR_RESPONSE: set[int] = set()


instagram_lock = asyncio.Lock()
lock = asyncio.Lock()


async def handle_message(
    message: InstagramMessage,
    db: UsersDBPort,
    llm: LLMPort,
    instagram: InstagramPort,
):
    user_status = await db.get_user_status_by_user_id(message.sender_id)
    if not user_status:
        await db.add_user(message)
    if user_status == "blocked":
        raise InvalidStatus(message.sender_username, user_status)

    async with lock:
        if message.sender_id in USERS_WAITING_FOR_RESPONSE:
            return
        USERS_WAITING_FOR_RESPONSE.add(message.sender_id)

    async with instagram_lock:
        thread_content = await instagram.get_thread(message.thread_id)
        llm_response: LLMResponse = await llm.get_ai_response(thread_content)
        await instagram.send_message(llm_response.message, message.thread_id)
        await db.update_user_status(message.sender_id, llm_response.status)

    async with lock:
        USERS_WAITING_FOR_RESPONSE.remove(message.sender_id)
