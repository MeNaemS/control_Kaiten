from fastapi import UploadFile
from typing import Any
from random import choice
import httpx
from .error_handler import handler
from .create_spaces import create_spaces
from .authorization import auth_token
from .create_board import create_board
from .create_card import create_card, card_attachment, card_children


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
    cards: list[dict[str, Any]] = []
    for space_id in {space['id'] for space in spaces}:
        board = await create_board(
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
