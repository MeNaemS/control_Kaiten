from dataclasses import dataclass
from .base_schema import BaseSchema


@dataclass
class File(BaseSchema):
    file: str
    filename: str
    file_type: str


@dataclass
class TododdlerRequest(BaseSchema):
    title: str
    description: str
    files: list[File]


@dataclass
class TododdlerCreateSpace(BaseSchema):
    pass