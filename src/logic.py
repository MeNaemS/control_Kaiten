from fastapi import HTTPException
from typing import Any, Coroutine
from src import find_by_key_value
from fastapi import UploadFile
import httpx
from src import fetch_configs_from_Kaiten


def handler(func: Coroutine) -> Coroutine:
    async def wrapper(**kwargs) -> str:
        try:
            async with httpx.AsyncClient() as session:
                return await func(session, **kwargs)
        except Exception as exception:
            raise HTTPException(status_code=500, detail=str(exception))

    return wrapper


async def create_bug_card(
    session: httpx.AsyncClient,
    kaiten_url: dict[str, Any],
    title: str,
    description: str
) -> dict[str, Any]:
    response = await session.post(
        f'{kaiten_url['url']}/api/latest/cards',
        headers={
            'Authorization': f'Bearer {kaiten_url['token']}'
        },
        json={
            'title': title,
            "board_id": kaiten_url['board_id'],
            'description': description
        }
    )
    response.raise_for_status()
    return response.json()


async def add_file(
    session: httpx.AsyncClient,
    kaiten_url: dict[str, Any],
    card_id: str | int,
    file: UploadFile
):
    response = await session.put(
        f'{kaiten_url['url']}/api/latest/cards/{card_id}/files',
        headers={'Authorization': f'Bearer {kaiten_url['token']}'},
        json={'card_id': card_id},
        files={'file': (file.filename, file.file.read())}
    )
    response.raise_for_status()


async def create_child_card(
    session: httpx.AsyncClient,
    kaiten: dict[str, Any],
    card_id: str | int
):
    response = await session.post(
        f'{kaiten['url']}/api/latest/cards/{card_id}/children',
        headers={
            'Authorization': f'Bearer {kaiten['token']}'
        },
        json={'card_id': card_id}
    )
    response.raise_for_status()


@handler
async def sending_requests(
    session: httpx.AsyncClient,
    config_url: str,
    title: str,
    description: str,
    files: list[UploadFile]
) -> str:
    try:
        # Getting configs from url
        kaiten_inf: dict[str, Any] = await fetch_configs_from_Kaiten(session, config_url)

        for kaiten in kaiten_inf['kaiten_urls']:
            # Creating a card
            card_id = await create_bug_card(session, kaiten, title, description)

            # Adding files to a card
            for file in files:
                await add_file(session, kaiten, card_id['id'], file)

            # Creating a child card
            await create_child_card(session, kaiten, card_id['id'])
        return f'{await find_by_key_value(kaiten, "primary", True)}/ticket/{card_id["id"]}'
    except httpx.HTTPStatusError as httpx_error:
        raise HTTPException(
            status_code=httpx_error.response.status_code,
            detail=httpx_error.response.text
        )
