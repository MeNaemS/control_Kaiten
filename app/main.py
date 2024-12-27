from fastapi import FastAPI, Form, UploadFile, File
from src.logic import fetch_kaiten_urls, create_card
from src.types import Any
from configs import get_configs

app: FastAPI = FastAPI()


@app.post('/api/tickets')
async def create_ticket(
    title: str = Form(...),
    description: str = Form(...),
    files: list[UploadFile] = File(...)
):
    configs: dict[str, Any] = await get_configs()
    Kaiten_urls: dict[str, Any] = await fetch_kaiten_urls(configs['settings']['default_endpoint'])
    return await create_card(Kaiten_urls, title, description, files)
