from aiohttp import ClientSession, ClientResponse, FormData
from asyncio import gather, Semaphore
from random import randint
from config import config
from cryptography.fernet import Fernet
from schemas.responses_schemas import KaitenToken
from schemas.tododdler_schemas import (
    BaseTododdler,
    ReTododdler,
    TododdlerRequest,
    TododdlerCardSchema,
    TododdlerCardAttachmentSchema,
    File
)
import base64


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


async def get_spaces(client: ClientSession, url: str) -> list[BaseTododdler]:
    response: list[BaseTododdler] = await client.get(url)
    response.raise_for_status()
    return await response.json()


async def create_space(client: ClientSession, url: str, title: str) -> BaseTododdler:
    response: BaseTododdler = await client.post(url, json={'title': title})
    response.raise_for_status()
    return await response.json()


async def create_spaces(
    client: ClientSession,
    url: str,
    title: str
) -> list[ReTododdler]:
    saved_spaces: list[BaseTododdler] = await get_spaces(client, url)
    primary_space: int = randint(0, 1)
    if title not in {space['title'] for space in saved_spaces}:
        spaces: list[BaseTododdler] = [
            await create_space(client, url, title) for _ in range(2)
        ]
    else:
        spaces: list[BaseTododdler] = [
            space for space in saved_spaces if space['title'] == title
        ][:2]
    for i in range(2):
        spaces[i]['primary'] = i == primary_space
    return spaces


async def create_board(
    client: ClientSession,
    url: str,
    space_id: int,
    title: str
) -> BaseTododdler:
    response: BaseTododdler = await client.post(
        url,
        json={
            'title': title,
            'space_id': space_id
        }
    )
    response.raise_for_status()
    return response.json()


async def attach_file(
    client: ClientSession,
    url: str,
    file: File
):
    data: FormData = FormData()
    data.add_field('file', base64.b64decode(file.file), filename=file.filename)
    response: TododdlerCardAttachmentSchema = client.post(url, data=data)
    response.raise_for_status()


async def create_card(
    client: ClientSession,
    url: str,
    board_id: int,
    card_data: TododdlerRequest,
    card_type: str
) -> TododdlerCardSchema:
    response: TododdlerCardSchema = await client.post(
        url,
        json={
            'board_id': board_id,
            'title': card_data.title,
            'description': card_data.description,
            'deadline': None,
            'type': card_type
        }
    )
    response.raise_for_status()
    return response.json()


async def create_child(
    client: ClientSession,
    url: str,
    child_card_id: int
):
    response: TododdlerCardAttachmentSchema = client.post(
        url,
        json={
            'card_id': child_card_id
        }
    )
    response.raise_for_status()


async def create_bug_child_card(
    client: ClientSession,
    url: str,
    space_primary: bool,
    board_id: int,
    card_data: TododdlerRequest,
    card_type: str
) -> TododdlerCardSchema | None:
    card: TododdlerCardSchema = await create_card(
        client,
        url,
        board_id,
        card_data,
        card_type
    )
    semaphore = Semaphore(8)
    async with semaphore:
        gather(
            *[
                attach_file(
                    client,
                    f'/api/card/{card['id']}/attachment',
                    file
                ) for file in card_data.files
            ]
        )
    child_card: TododdlerCardSchema = await create_card(
        client,
        url,
        board_id,
        card_data,
        card_type
    )
    await create_child(client, url, child_card['id'])
    return card['id'] if space_primary else None
