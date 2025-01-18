from fastapi import APIRouter, Form, Depends, Request
from typing import Annotated
from dependency.validate import validate_tododdler_data
from schemas.tododdler_schemas import BaseTododdler, ReTododdler
from services.http_requests import (
    create_spaces,
    create_board,
    create_bug_child_card
)
from config import config

kaiten_router: APIRouter = APIRouter(prefix='/api/tickets', tags=['tickets'])


@kaiten_router.post('')
async def create_tickets(
    request: Request,
    tododdler_data: Annotated[dict, Depends(validate_tododdler_data)] = Form(...)
) -> str:
    primary_card: int | None = None
    spaces: list[ReTododdler] = await create_spaces(request.app.state.client, '/api/space', tododdler_data.title)
    for space in spaces:
        board: BaseTododdler = await create_board(
            request.app.state.client,
            '/api/board',
            space['id'],
            tododdler_data.title
        )
        primary_card = await create_bug_child_card(
            request.app.state.client,
            '/api/card',
            space['primary'],
            board['id'],
            tododdler_data,
            'bug'
        ) if primary_card is None else primary_card
    return f'{config.urls.default_endpoint}/ticket/{primary_card}'
