from pydantic import BaseModel
from .param import Param
from typing import Optional


class Command(BaseModel):
    name: str
    method: str
    suffix: str
    params: list[Param] = []
    headers: list[Param] = []
    body: Optional[str]
    pre_process: str
    post_process: str
