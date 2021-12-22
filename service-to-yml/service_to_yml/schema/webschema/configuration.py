from pydantic import BaseModel

from .param import Param


class Configuration(BaseModel):
    name: str
    base_url: str
    proxy: bool = False
    insecure: bool = False
    context_key: str
    headers: list[Param] = []
