from fastapi import FastAPI, Form, UploadFile, File, APIRouter
from typing import Any
from src import sending_requests, get_configs

app: FastAPI = FastAPI()
router: APIRouter = APIRouter()


@router.post('/api/tickets', tags=['tickets'])
async def create_ticket(
    title: str = Form(...),
    description: str = Form(...),
    files: list[UploadFile] = File(...)
):
    configs: dict[str, Any] = await get_configs()
    return await sending_requests(
        config=configs['settings'],
        title=title,
        description=description,
        files=files
    )


app.include_router(router)
