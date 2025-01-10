from dataclasses import dataclass
from typing import List
from adaptix import Retort

retort: Retort = Retort()


@dataclass
class FileContent:
    read: bytearray


@dataclass
class FileData:
    filename: str
    file: FileContent


@dataclass
class CardInfo:
    title: str
    description: str
    files: List[FileData]
