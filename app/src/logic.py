from src.types import HTTPException, Any
from src import find_by_key_value
from fastapi import UploadFile
import aiohttp
import httpx


async def fetch_kaiten_urls(url: str) -> dict[str, Any]:
    try:
        async with aiohttp.ClientSession() as session:
            response = await session.get(url)
            response.raise_for_status()
            return await response.json()
    except Exception as exception:
        raise HTTPException(status_code=500, detail=f'Error accessing the specified endpoint: {exception}')


async def create_kaiten_card(kaiten_inf: dict[str, Any], title: str, description: str) -> str:
    try:
        async with aiohttp.ClientSession() as session:
            response = await session.post(
                f'{kaiten_inf['url']}/api/latest/cards',
                headers={
                    'Authorization': f'Bearer {kaiten_inf['token']}'
                },
                json={
                    'title': title,
                    "board_id": kaiten_inf['board_id'],
                    'description': description
                }
            )
            response.raise_for_status()
            return await response.json()
    except aiohttp.ClientResponseError as aiohttp_error:
        raise HTTPException(status_code=aiohttp_error.status, detail=aiohttp_error.message)
    except Exception as exception:
        raise HTTPException(status_code=500, detail=f'Error creating a child ticket: {exception}')


async def upload_file_to_kaiten(kaiten_inf: dict[str, Any], card_id: int, file: UploadFile):
    try:
        async with httpx.AsyncClient() as session:
            response = await session.put(
                f'{kaiten_inf['url']}/api/latest/cards/{card_id}/files',
                headers={'Authorization': f'Bearer {kaiten_inf['token']}'},
                json={'card_id': card_id},
                files={'file': (file.filename, file.file.read())}
            )
            response.raise_for_status()
    except httpx.HTTPError as httpx_error:
        raise HTTPException(status_code=response.status, detail=httpx_error.message)
    except Exception as exception:
        raise HTTPException(
            status_code=500,
            detail=f'Error uploading files to Kaiten: {exception}'
        )


async def add_children_to_kaiten(kaiten_inf: dict[str, Any], card_id: int):
    try:
        async with aiohttp.ClientSession() as session:
            response = await session.post(
                f'{kaiten_inf['url']}/api/latest/cards/{card_id}/children',
                headers={
                    'Authorization': f'Bearer {kaiten_inf['token']}'
                },
                json={'card_id': card_id}
            )
            response.raise_for_status()
    except aiohttp.ClientResponseError as aiohttp_error:
        raise HTTPException(status_code=aiohttp_error.status, detail=aiohttp_error.message)
    except Exception as exception:
        raise HTTPException(status_code=500, detail=f'Error creating a child ticket: {exception}')


async def create_card(Kaiten_urls: list, title: str, description: str, files: UploadFile) -> str:
    for kaiten_inf in Kaiten_urls['kaiten_urls']:
        card_id = await create_kaiten_card(kaiten_inf, title, description)
        for file in files:
            await upload_file_to_kaiten(kaiten_inf, card_id['id'], file)
        await add_children_to_kaiten(kaiten_inf, card_id['id'])
    return f'{await find_by_key_value(Kaiten_urls["kaiten_urls"], "primary", True)}/ticket' +\
        f'/{card_id["id"]}'
