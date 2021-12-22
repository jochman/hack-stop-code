from pydantic import BaseModel

from .command import Command
from .configuration import Configuration


class Integration(BaseModel):
    configuration: Configuration
    commands: list[Command]
