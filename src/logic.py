from fastapi import HTTPException, UploadFile
from typing import Any, Coroutine
from cryptography.fernet import Fernet
from random import choice
import httpx
import json
from src import get_spaces_data


def handler(func: Coroutine) -> Coroutine:
    """ Error handler.  """
    async def wrapper(**kwargs) -> str:
        """
        Creating an asynchronous session with error handling.
        **kwargs::
            — config: dict[str, str] — the link from where the data should be parsed.
            — title: str — name of cards.
            — description: str — description of cards.
            — files: list[UploadFile] — array of files.
        """
        try:
            async with httpx.AsyncClient() as session:
                return await func(session, **kwargs)
        except httpx.HTTPStatusError as httpx_error:
            raise HTTPException(
                status_code=400,
                detail=httpx_error.response.text
            )
        except Exception as exception:
            raise HTTPException(status_code=500, detail=str(exception))

    return wrapper


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
    with open('./configs/spaces.json', 'w') as file:
        json.dump(response.json(), file, indent=2)


async def create_board(
    session: httpx.AsyncClient,
    token: str,
    default_url: str,
    space_id: int,
    title: str = 'board'
):
    response: httpx.Response = await session.post(
        f'{default_url}/api/board',
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        },
        json={
            'space_id': space_id,
            'title': title
        }
    )
    response.raise_for_status()
    return response.json()


async def create_card(
    session: httpx.AsyncClient,
    token: str,
    default_url: str,
    board_id: int,
    title: str,
    description: str
):
    response: httpx.Response = await session.post(
        f'{default_url}/api/card',
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        },
        json={
            'board_id': board_id,
            'title': title,
            'description': description
        }
    )
    response.raise_for_status()
    return response.json()


async def card_attachment(
    session: httpx.AsyncClient,
    token: str,
    default_url: str,
    card_id: int,
    file: UploadFile
):
    response: httpx.Response = await session.post(
        f'{default_url}/api/card/{card_id}/attachment',
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        },
        files={'file': {'filename': file.filename, 'file': file.file.read()}}
    )
    response.raise_for_status()


async def card_children(
    session: httpx.AsyncClient,
    token: str,
    default_url: str,
    card_id: int,
):
    response: httpx.Response = await session.post(
        f'{default_url}/api/card/{card_id}/children',
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
    )
    response.raise_for_status()


@handler
async def sending_requests(
    session: httpx.AsyncClient,
    config: dict[str, str],
    title: str,
    description: str,
    files: list[UploadFile]
) -> str:
    token: dict[str, Any] = await auth_token(session, config)
    spaces: list[dict[str, Any]] = await create_spaces(
        session=session,
        token=token['access_token'],
        default_url=config['default_endpoint'],
        titles=[f'space_{i}' for i in range(1, 3)]
    )
    await save_spaces(session, token['access_token'], config['default_endpoint'])
    cards: list[dict[str, Any]] = []
    for space_id in {space['id'] for space in spaces}:
        board = create_board(
            session,
            token['access_token'],
            config['default_endpoint'],
            space_id
        )
        for _ in range(2):
            cards.append(
                await create_card(
                    session,
                    token['access_token'],
                    config['default_endpoint'],
                    board['id'],
                    title,
                    description
                )
            )
            for file in files:
                await card_attachment(
                    session,
                    token['access_token'],
                    config['default_endpoint'],
                    cards[-1]['id'],
                    file
                )
            await card_children(
                session,
                token['access_token'],
                config['default_endpoint'],
                cards[-1]['id']
            )
    return f'{config['default_endpoint']}/ticket/{choice(cards)['id']}'
