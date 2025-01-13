from fastapi import UploadFile
from typing import Any
from random import choice
from asyncio import gather
import httpx
from .error_handler import handler, async_semaphore
from .create_spaces import create_spaces
from .authorization import auth_token
from .create_board import create_board
from .create_card import create_card, card_attachment, card_children


@async_semaphore
async def async_files(
    session: httpx.AsyncClient,
    token: str,
    default_endpoint: str,
    card_id: int,
    file: UploadFile
):
    await card_attachment(
        session,
        token,
        default_endpoint,
        card_id,
        file
    )


async def async_cards(
    board_id: int,
    session: httpx.AsyncClient,
    token: str,
    default_endpoint: str,
    title: str,
    description: str,
    type_card: str,
    files: list[UploadFile]
):
    card = await create_card(
        session,
        token,
        default_endpoint,
        board_id,
        title,
        description,
        type_card
    )
    await gather(
        *[
            async_files(
                session,
                token,
                default_endpoint,
                card['id'],
                file
            ) for file in files
        ]
    )
    await card_children(
        session,
        token,
        default_endpoint,
        card['id']
    )
    return card['id']


async def async_spaces(
    space_id: int,
    session: httpx.AsyncClient,
    token: str,
    default_endpoint: str,
    title: str,
    description: str,
    files: list[UploadFile]
):
    board: dict[str, Any] = await create_board(
        session,
        token,
        default_endpoint,
        space_id
    )
    cards = await gather(
        *[
            async_cards(
                board['id'],
                session,
                token,
                default_endpoint,
                title,
                description,
                type_card,
                files
            ) for type_card in ['card', 'bug']
        ]
    )
    return cards


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
    cards: list[dict[str, Any]] = await gather(
        *[
            async_spaces(
                space_id,
                session,
                token['access_token'],
                config['default_endpoint'],
                title,
                description,
                files
            ) for space_id in {space['id'] for space in spaces}
        ]
    )
    return f'{config['default_endpoint']}/ticket/{choice(cards)}'
