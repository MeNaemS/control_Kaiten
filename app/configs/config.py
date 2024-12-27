from typing import Any
from json import load

with open('.\\configs\\config.json', 'r', encoding='UTF-8') as file:
    config: Any = load(file)
