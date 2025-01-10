from typing import Any
from dotenv import load_dotenv
from os import getenv
import tomli
import json
from .error_handler import config_handler

load_dotenv()


@config_handler
async def get_configs(path: str = getenv('CONFIG_PATH')) -> dict[str, Any]:
    with open(path, 'rb') as toml_file:
        return tomli.load(toml_file)


@config_handler
async def get_spaces_data(path: str = getenv('SPACES_PATH')) -> list[dict[str, Any]]:
    with open(path, 'r') as file:
        return json.load(file)


@config_handler
async def spaces_to_json(response_json: dict[str, Any], path: str = getenv('SPACES_PATH')):
    with open(path, 'w') as file:
        json.dump(response_json, file, indent=2)
