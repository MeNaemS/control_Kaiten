from aiohttp import ClientSession, ClientResponse
from random import choice
from config import config
from cryptography.fernet import Fernet
from schemas.responses_schemas import KaitenToken


async def get_data_from_Kaiten(fernet_key: Fernet) -> KaitenToken:
    async with ClientSession() as session:
        response: ClientResponse = await session.post(
            config.urls.auth_url,
            data={
                'grant_type': 'client_credentials',
                'client_id': config.secret.clientId,
                'client_secret': fernet_key.decrypt(config.secret.clientSecret.encode()).decode()
            }
        )
        response.raise_for_status()
        return await response.json()


async def create_space(client: ClientSession, url: str, title: str):
    return await client.post(url, json={'title': title})


async def create_spaces(client: ClientSession, url: str, title: str):
    return await create_space(client, url, title)
