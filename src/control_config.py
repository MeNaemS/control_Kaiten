from typing import Any
from tomli import load
import httpx


async def get_configs(path: str = './configs/config.toml') -> dict[str, Any]:
    try:
        with open(path, 'rb') as toml_file:
            return load(toml_file)
    except Exception as exception:
        raise RuntimeError(f'Error loading data from configuration: {exception}')


async def fetch_configs_from_Kaiten(session: httpx.AsyncClient, url: str) -> dict[str, Any]:
    response = await session.get(url)
    response.raise_for_status()
    return response.json()
