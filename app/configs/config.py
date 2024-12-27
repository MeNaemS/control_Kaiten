from tomli import load
from src.types import Any

async def get_configs(path: str = '.\\configs\\config.toml') -> dict[str, Any]:
    try:
        with open(path, 'rb') as toml_file:
            return load(toml_file)
    except Exception as exception:
        raise RuntimeError(f'Error loading data from configuration: {exception}')
