from fastapi import File
from typing import Any
from requests import get, Response, post, put
from configs import config


def get_Kaiten_urls(url: str = config['default_endpoint']) -> dict[str, Any]:
    response: Response = get(url)
    return response.json()


def create_card(Kaiten_urls: list, title: str, description: str, files: File):
    for card in Kaiten_urls['kaiten_urls']:
        response: Response = post(
            f'{card['url']}/api/latest/cards',
            headers={
                'Authorization': f'Bearer {card['token']}'
            },
            json={
                'title': title,
                "board_id": card['board_id'],
                'description': description
            }
        )
        tic_id = response.json()['id']
        for file in files:
            response = put(
                f'{card['url']}/api/latest/cards/{tic_id}/files',
                json={'id': tic_id},
                files={'file': file.file}
            )
        response = post(
            f'{card['url']}/api/latest/cards/{tic_id}/children',
            headers={
                'Authorization': f'Bearer {card['token']}'
            },
            json={'card_id': tic_id}
        )
    return tic_id

