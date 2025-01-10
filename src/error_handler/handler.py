from fastapi import HTTPException
from typing import Coroutine, Any
import httpx


def handler(func: Coroutine) -> Coroutine:
    """ Error handler.  """
    async def wrapper(**kwargs) -> str:
        """
        Creating an asynchronous session with error handling.
        **kwargs::
            — config: dict[str, str] — the link from where the data should be parsed.
            — title: str — name of cards.
            — description: str — description of cards.
            — files: list[UploadFile] — array of files.
        """
        try:
            async with httpx.AsyncClient() as session:
                return await func(session, **kwargs)
        except httpx.HTTPStatusError as httpx_error:
            raise HTTPException(
                status_code=400,
                detail={
                    'error': str(httpx_error),
                    'response': httpx_error.response.text
                }
            )
        except Exception as exception:
            raise HTTPException(status_code=500, detail=str(exception))

    return wrapper


def config_handler(func: Coroutine) -> Coroutine:
    async def wrapper(**kwargs) -> Any:
        try:
            return await func(**kwargs)
        except Exception as exception:
            raise HTTPException(status_code=500, detail=str(exception))

    return wrapper
