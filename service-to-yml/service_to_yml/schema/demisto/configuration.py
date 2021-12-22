from pydantic import BaseModel


class Configuration(BaseModel):
    display: str
    defaultvalue: str = ''
    name: str
    type: int = 0
    required: bool = False
    hidden: bool = False
    additionalinfo: str = ''
