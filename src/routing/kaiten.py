from fastapi import APIRouter, Form, Depends, Request
from typing import Annotated
from dependency.validate import validate_tododdler_data
from services.http_requests import (
    create_spaces
)

kaiten_router: APIRouter = APIRouter(prefix='/api/tickets', tags=['tickets'])


@kaiten_router.post('')
async def create_tickets(
    request: Request,
    tododdler_data: Annotated[dict, Depends(validate_tododdler_data)] = Form(...)
):
    ex = await create_spaces(request.app.state.client, '/api/space', tododdler_data.title)
    return await ex.json()
