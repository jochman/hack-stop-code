from pydantic import BaseModel

from .param import Param


class Configuration(BaseModel):
    name: str
    base_url: str
    context_key: str
    headers: list[Param] = []
