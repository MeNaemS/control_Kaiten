from typing import Coroutine, Any
from asyncio import gather
import httpx
from src.error_handler import async_semaphore


@async_semaphore
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
        """
        # Deleting spaces with an existing name
        await gather(
            *[
                delete_space(
                    kwargs['session'], kwargs['token'], kwargs['default_url'], space['id']
                ) for space in await get_spaces(
                    kwargs['session'],
                    kwargs['token'],
                    kwargs['default_url']
                ) if space['title'] in kwargs['titles']
            ]
        )
        # Creating Spaces
        return await gather(
            *[
                func(
                    kwargs['session'], kwargs['token'], kwargs['default_url'], title
                ) for title in kwargs['titles']
            ]
        )

    return wrapper


@spaces
@async_semaphore
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


async def get_spaces(
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
    return response.json()
