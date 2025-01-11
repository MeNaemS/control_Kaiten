from typing import Any
from dotenv import load_dotenv
from os import getenv
import tomli
from .error_handler import config_handler

load_dotenv()


@config_handler
async def get_configs(path: str = getenv('CONFIG_PATH')) -> dict[str, Any]:
    with open(path, 'rb') as toml_file:
        return tomli.load(toml_file)
