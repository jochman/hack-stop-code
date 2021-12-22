from pydantic import BaseModel


class Param(BaseModel):
    key: str
    value: str
    required: bool = False
    hidden: bool = True
