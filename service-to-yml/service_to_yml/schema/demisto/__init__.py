from .argument import Argument
from .command import Command
from .configuration import Configuration
from .integration import Integration, CommonFields
from .output import Output
from .script import Script

class Demisto:
    Argument = Argument
    Command = Command
    Configuration = Configuration
    Integration = Integration
    CommonFields = CommonFields
    Output = Output
    Script = Script
    