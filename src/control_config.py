from fastapi import HTTPException
from typing import Any, Coroutine
import tomli
import json
import httpx


def config_handler(func: Coroutine) -> Coroutine:
    async def wrapper(**kwargs) -> Any:
        try:
            return await func(**kwargs)
        except Exception as exception:
            raise HTTPException(status_code=500, detail=str(exception))

    return wrapper


@config_handler
async def get_configs(path: str = './configs/config.toml') -> dict[str, Any]:
    with open(path, 'rb') as toml_file:
        return tomli.load(toml_file)


@config_handler
async def get_spaces_data(path: str = './configs/spaces.json') -> list[dict[str, Any]]:
    with open(path, 'r') as file:
        return json.load(file)
