from fastapi import FastAPI, Form, UploadFile, File
from typing import Any
from src import sending_requests
from configs import get_configs

app: FastAPI = FastAPI()


@app.post('/api/tickets')
async def create_ticket(
    title: str = Form(...),
    description: str = Form(...),
    files: list[UploadFile] = File(...)
):
    configs: dict[str, Any] = await get_configs()
    return await sending_requests(
        config_url=configs['settings']['default_endpoint'],
        title=title,
        description=description,
        files=files
    )
