from typing import Optional

from pydantic import BaseModel, Field


class Argument(BaseModel):
    name: str
    required: bool = False
    default: bool = False
    description: str = ''
    auto: Optional[bool]
    predefined: list[str] = []
    isArray: bool = False
    defaultValue: str = ''
    secret: bool = False
    deprecated: bool = False
