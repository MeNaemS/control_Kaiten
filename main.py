from fastapi import FastAPI, Form, UploadFile, File
from typing import Any
from src import sending_requests, get_configs

app: FastAPI = FastAPI()


@app.post('/api/tickets')
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
