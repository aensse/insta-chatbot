import asyncio
from typing import Annotated

from fastapi import BackgroundTasks, Depends, FastAPI, Request

from app.core.config import files, settings
from app.core.logger import setup_logging
from app.infrastructure.async_queue import AsyncQueue
from app.infrastructure.db_config import AsyncSessionLocal, Base, engine
from app.infrastructure.db_queries import ThreadsQueries
from app.infrastructure.grok_client import GrokClient
from app.infrastructure.instagram_client import InstagramClient
from app.infrastructure.schemas import UserMessage
from app.services.ig_client_factory import Credentials, create_client
from app.services.message_responder import MessageResponderDeps, send_message_to_bot


async def get_threads_queries():
    session = AsyncSessionLocal()
    try:
        yield ThreadsQueries(session)
    finally:
        await session.close()


async def get_ai_client() -> GrokClient:
    return GrokClient(settings.xai_api_key.get_secret_value(), settings.grok_model, files.get_instructions)


async def lifespan(_app: FastAPI):

    setup_logging()

    credentials = Credentials(settings.ig_username, settings.ig_password, settings.ig_secret)
    cl = await create_client(files.session_file, credentials)

    q = AsyncQueue(asyncio.Queue())
    task = asyncio.create_task(q.consumer())

    app.state.ig = InstagramClient(cl)
    app.state.q = q

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    task.cancel()
    await engine.dispose()


app = FastAPI(lifespan=lifespan)


@app.post("/api/message")
async def process_message(
    request: Request,
    message: UserMessage,
    background_task: BackgroundTasks,
    db: Annotated[ThreadsQueries, Depends(get_threads_queries)],
    ai: Annotated[GrokClient, Depends(get_ai_client)],
):
    task = send_message_to_bot
    deps = MessageResponderDeps(message, db, ai, request.app.state.ig, request.app.state.q)

    background_task.add_task(task, deps)
    return {"message": "Notification sent to bot in background."}
