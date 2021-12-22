from typing import Optional

from pydantic import BaseModel, Field

from .command import Command

code = open('unified.py').read(

)
class Script(BaseModel):
    script: Optional[str] = code
    type: str = 'python'
    dockerimage: str = 'demisto/python3:3.9.7.24076'
    dockerimage45: Optional[str]
    alt_dockerimages: Optional[str]
    isfetch: bool = False
    longRunning: bool = False
    longRunningPort: Optional[str]
    ismappable: bool = False
    isremotesyncin: bool = False
    isremotesyncout: bool = False
    commands: list[Command] = []
    runonce: bool = False
    subtype: str = 'python3'
    feed: bool = False
    isFetchSamples: bool = False
    resetContext: bool = False
