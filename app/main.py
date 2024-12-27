from fastapi import FastAPI, Form, UploadFile, File
from typing import Any
from src.logic import get_Kaiten_urls, create_card
from src.utils import find_by_key_value

app: FastAPI = FastAPI()

@app.post('/api/tickets')
async def create_ticket(
    title: str = Form(...),
    description: str = Form(...),
    files: list[UploadFile] = File(...)
):
    Kaiten_urls: dict[str, Any] = get_Kaiten_urls()
    return f'{find_by_key_value(Kaiten_urls["kaiten_urls"], "primary", True)["url"]}/ticket/' +\
        f'{create_card(Kaiten_urls, title, description, files)}'
