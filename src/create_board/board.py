import httpx


async def create_board(
    session: httpx.AsyncClient,
    token: str,
    default_url: str,
    space_id: int,
    title: str = 'board'
):
    response: httpx.Response = await session.post(
        f'{default_url}/api/board',
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        },
        json={
            'space_id': space_id,
            'title': title
        }
    )
    response.raise_for_status()
    return response.json()
