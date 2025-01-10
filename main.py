from fastapi import FastAPI, Form, UploadFile, File, APIRouter, HTTPException
from typing import Any
from src import sending_requests, get_configs, retort, CardInfo
import base64

app: FastAPI = FastAPI()
router: APIRouter = APIRouter()


@router.post('/api/tickets', tags=['tickets'])
async def create_ticket(
    title: str = Form(...),
    description: str = Form(...),
    files: list[UploadFile] = File(...)
) -> str:
    try:
        data = retort.load(
            {
                'title': title,
                'description': description,
                'files': [
                    {
                        'filename': file.filename,
                        'file': {
                            'read': base64.b64encode(file.file.read()).decode('ascii')
                        }
                    } for file in files
                ]
            },
            CardInfo
        )
        configs: dict[str, Any] = await get_configs()
        return await sending_requests(
            config=configs['settings'],
            title=data.title,
            description=data.description,
            files=data.files
        )
    except Exception as exception:
        raise HTTPException(status_code=400, detail=str(exception))


app.include_router(router)
