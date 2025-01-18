from dataclasses import dataclass
from .base_schema import BaseSchema


@dataclass
class Headers(BaseSchema):
    ContentType: str
    Authorization: str


@dataclass
class KaitenToken(BaseSchema):
    access_token: str
    expires_in: int
    refresh_expires_in: int
    token_type: str
    not_before_policy: int
    scope: str
