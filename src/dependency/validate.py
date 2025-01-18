from fastapi import UploadFile
from adaptix import Retort
import base64
from schemas.tododdler_schemas import TododdlerRequest

retort = Retort()


async def validate_tododdler_data(title, description, files: list[UploadFile]) -> TododdlerRequest:
    return retort.load(
        {
            'title': title,
            'description': description,
            'files': [
                {
                    'file': base64.b64encode(await file.read()).decode(),
                    'filename': file.filename,
                    'file_type': file.headers['content-type']
                } for file in files
            ]
        },
        TododdlerRequest
    )
