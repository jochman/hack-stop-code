from typing import List, Optional

from pydantic import BaseModel, Field

from .command import Command
from .configuration import Configuration
from .script import Script


class CommonFields(BaseModel):
    id: str
    version: int = -1


class Integration(BaseModel):
    commonfields: CommonFields
    name: str
    display: str
    deprecated: bool = False
    beta: bool = False
    category: str
    fromversion: str = '6.5.0'
    toversion: Optional[str]
    image: Optional[str]
    description: str = ''
    defaultmapperin: Optional[str]
    defaultmapperout: Optional[str]
    defaultclassifier: Optional[str]
    detaileddescription: str = ''
    autoconfiginstance: bool = False
    configuration: list[Configuration]
    script: Script
    system: bool = False
    hidden: bool = False
    versionedfields: str = ''
    defaultEnabled: bool = False
    tests: list[str] = ['no tests']
    scriptNotVisible: bool = False
    autoUpdateDockerImage: bool = True
