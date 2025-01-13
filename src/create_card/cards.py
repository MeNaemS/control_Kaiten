from fastapi import UploadFile
from PIL import Image
from io import BytesIO
import base64
import httpx


async def create_card(
    session: httpx.AsyncClient,
    token: str,
    default_url: str,
    board_id: int,
    title: str,
    description: str,
    type_card: str
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
            'description': description,
            'type': type_card
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
        data=file.file.read
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
