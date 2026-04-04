from dataclasses import dataclass

import pyotp
from aiograpi import Client
from aiograpi.exceptions import LoginRequired
from aiopath import Path

DEVICE = {
    "app_version": "310.0.0.40.111",
    "android_version": 14,
    "android_release": "14.0.0",
    "dpi": "560dpi",
    "resolution": "1440x3200",
    "manufacturer": "samsung",
    "device": "SM-S928B",
    "model": "SM-S928B",
    "cpu": "arm64-v8a",
    "version_code": "310040111",
    "phone_manufacturer": "samsung",
    "phone_model": "SM-S928B",
    "hardware": "q2q",
    "product": "q2qxx",
    "build": "q2q-user 14 UP1A.231005.007 S928BXXU1AWF5 release-keys",
    "fingerprint": "samsung/q2qxx/q2q:14/UP1A.231005.007/S928BXXU1AWF5:user/release-keys",  # noqa: E501
    "brand": "samsung",
    "device_id": "android-7a9b3c2d1e4f8560",
    "phone_id": "7a9b3c2d-1e4f-8560-9d8e-f0123456789a",
    "uuid": "550e8400-e29b-41d4-a716-446655440000",
    "client_session_id": "550e8400-e29b-41d4-a716-446655440000",
    "ig_android_id": "android-7a9b3c2d1e4f8560",
}

USER_AGENT = "Instagram 310.0.0.40.111 Android (34/14.0.0; 560dpi; 1440x3200; samsung; SM-S928B; q2q; q2qxx; pl_PL; 310040111)"  # noqa: E501

# TODO: move that data into YAML config file


@dataclass
class Credentials:
    username: str
    password: str
    secret: str | None


async def login_via_credentials(
    cl: Client, username: str, password: str, secret: str | None
) -> None:
    if secret:
        code = pyotp.TOTP(secret)
        await cl.login(username, password, verification_code=code.now())
        return
    await cl.login(username, password)


async def login_via_session(
    cl: Client, session: dict, username: str, password: str, secret: str | None
) -> None:
    cl.set_settings(session)
    cl.username = username
    try:
        await cl.get_timeline_feed()
    except LoginRequired:
        old_session = cl.get_settings()
        cl.set_settings({})
        cl.set_uuids(old_session["uuids"])
        await login_via_credentials(cl, username, password, secret)


async def create_client(
    session_file: Path, username: str, password: str, secret: str | None
) -> Client:
    cl = Client()
    cl.delay_range = [3, 7]
    cl.set_device(DEVICE)
    cl.set_user_agent(USER_AGENT)
    if session_file.exists():
        session = cl.load_settings(session_file)
        if isinstance(session, dict):
            await login_via_session(cl, session, username, password, secret)
            return cl
    await login_via_credentials(cl, username, password, secret)
    cl.dump_settings(session_file)
    return cl
