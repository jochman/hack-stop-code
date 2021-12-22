from pydantic import BaseModel
from typing import Any

class Configuration(BaseModel):
    display: str
    defaultvalue: Any = ''
    name: str
    type: int = 0
    required: bool = False
    hidden: bool = False
    additionalinfo: str = ''
