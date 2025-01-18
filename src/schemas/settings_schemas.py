from dataclasses import dataclass
from .base_schema import BaseSchema


@dataclass
class Secret(BaseSchema):
    fernet_key: str
    clientId: str
    clientSecret: str


@dataclass
class Urls(BaseSchema):
    default_endpoint: str
    auth_url: str


@dataclass
class ConfigSchema(BaseSchema):
    secret: Secret
    urls: Urls
