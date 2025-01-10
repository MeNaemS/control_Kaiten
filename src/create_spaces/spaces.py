from typing import Coroutine, Any
import httpx
from src import get_spaces_data, spaces_to_json


async def delete_space(
    session: httpx.AsyncClient,
    token: str,
    default_url: str,
    entity_id: str
):
    response: httpx.Response = await session.delete(
        f'{default_url}/api/space/{entity_id}',
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
    )
    response.raise_for_status()


def spaces(func: Coroutine) -> Coroutine:
    async def wrapper(**kwargs) -> list[dict[str, Any]]:
        """
        Creating spaces.
        **kwargs::
            — session: httpx.AsyncClient — asynchronous session for sending requests
            — token: str — token for access.
            — default_url: str — default url to which requests are sent.
            — titles: list[str] — array of names for spaces.
            — path: str = './configs/spaces.json' — path to file with spaces.
        """
        path: str = kwargs.get('path', './configs/spaces.json')
        spaces_data: Any = await get_spaces_data(path=path)
        if spaces_data != []:
            for space in spaces_data:
                if space['title'] in kwargs['titles']:
                    await delete_space(
                        kwargs['session'], kwargs['token'], kwargs['default_url'], space['id']
                    )
        spaces_data: list[dict[str, Any]] = []
        for title in kwargs['titles']:
            spaces_data.append(
                await func(kwargs['session'], kwargs['token'], kwargs['default_url'], title)
            )
        return spaces_data

    return wrapper


@spaces
async def create_spaces(
    session: httpx.AsyncClient,
    token: str,
    default_url: str,
    title: str
) -> dict[str, Any]:
    response: httpx.Response = await session.post(
        f'{default_url}/api/space',
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        },
        json={
            'title': title
        }
    )
    response.raise_for_status()
    return response.json()


async def save_spaces(
    session: httpx.AsyncClient,
    token: str,
    default_url: str,
):
    response: httpx.Response = await session.get(
        f'{default_url}/api/space',
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
    )
    response.raise_for_status()
    await spaces_to_json(response_json=response.json())
