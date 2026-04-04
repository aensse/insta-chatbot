from aiograpi import Client
from aiograpi.types import DirectMessage

from app.domain.models import InstagramThread


class AiograpiAdapter:
    def __init__(self, cl: Client) -> None:
        self.cl = cl

    async def refresh(self) -> None:
        self.cl.get_timeline_feed()

    async def get_thread(self, thread_id: int) -> list[InstagramThread]:
        thread: list[DirectMessage] = await self.cl.direct_messages(thread_id=thread_id)
        thread.reverse()
        to_exclude = {
            "id",
            "user_id",
            "thread_id",
            "timestamp",
            "item_type",
            "is_shh_mode",
            "reactions",
            "reply",
            "link",
            "animated_media",
            "media",
            "visual_media",
            "media_share",
            "reel_share",
            "story_share",
            "felix_share",
            "xma_share",
            "clip",
            "placeholder",
        }
        clean_thread = []
        clean_thread.extend(
            InstagramThread(**message.model_dump(exclude=to_exclude))
            for message in thread
        )
        return clean_thread

    async def send_message(self, message: str, thread_id: int) -> None:
        await self.cl.direct_send(text=message, thread_ids=[thread_id])
