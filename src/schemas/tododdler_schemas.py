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
class BaseTododdler(BaseSchema):
    id: 204
    title: str
    createdAt: str
    updatedAt: str


@dataclass
class ReTododdler(BaseTododdler):
    primary: bool


@dataclass
class TododdlerLinks(BaseSchema):
    leftCardId: int
    rightCardId: int
    linkType: str
    createdAt: str
    updatedAt: str


@dataclass
class TododdlerCardSchema(BaseSchema):
    board_id: int
    id: int
    title: str
    description: str
    creatorId: str
    deadline: str
    type: str
    createdAt: str
    updatedAt: str
    links: list[TododdlerLinks]


@dataclass
class TododdlerAttachemtns(BaseSchema):
    id: str
    filename: str
    fileType: str
    url: str


@dataclass
class TododdlerCardAttachmentSchema(TododdlerCardSchema):
    attachemnts: list[TododdlerAttachemtns]
