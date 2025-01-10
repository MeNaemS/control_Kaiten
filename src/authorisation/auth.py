from typing import Any
from cryptography.fernet import Fernet
import httpx


async def auth_token(
    session: httpx.AsyncClient,
    config: dict[str, str]
) -> dict[str, Any]:
    decoder: Fernet = Fernet(config['fernet_key'])
    response: httpx.Response = await session.post(
        config['auth_url'],
        data={
            'grant_type': 'client_credentials',
            'client_id': config['clientId'],
            'client_secret': decoder.decrypt(config['clientSecret'].encode()).decode()
        }
    )
    response.raise_for_status()
    return response.json()
