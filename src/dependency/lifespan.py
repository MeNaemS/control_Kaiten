from contextlib import asynccontextmanager
from fastapi import FastAPI
from schemas.responses_schemas import KaitenToken
from services.http_requests import get_data_from_Kaiten
from services.fernet_key import get_key
from config import config
import aiohttp


@asynccontextmanager
async def lifespan(app: FastAPI):
    response_json: KaitenToken = await get_data_from_Kaiten(await get_key())
    app.state.client: aiohttp.ClientSession = aiohttp.ClientSession(
        headers={
            "Content-Type": "application/json",
            "Authorization": f"{response_json['token_type']} {response_json['access_token']}"
        },
        base_url=config.urls.default_endpoint
    )
    yield
    await app.state.client.close()
