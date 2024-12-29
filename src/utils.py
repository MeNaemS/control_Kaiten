from typing import Any


async def find_by_key_value(dictionary: list[dict[str, Any]], key: str, value: Any) -> dict[str, Any]:
    result = None
    for Kaiten_dict in dictionary:
        result = Kaiten_dict
        for key_dict, value_dict in Kaiten_dict.items():
            if key_dict == key and value_dict == value:
                return result
