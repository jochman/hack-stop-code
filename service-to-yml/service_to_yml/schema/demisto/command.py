from typing import Optional

from pydantic import BaseModel

from .argument import Argument
from .output import Output


class Command(BaseModel):
    name: str
    execution: bool = False
    description: str = ''
    deprecated: bool = False
    system: bool = False
    arguments: Optional[list[Argument]]
    outputs: Optional[list[Output]] = []
    timeout: Optional[int]
    hidden: bool = False
    polling: bool = False
