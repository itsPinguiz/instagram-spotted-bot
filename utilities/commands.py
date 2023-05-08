from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from botConsole import BotConsole

from dataclasses import dataclass
from typing import List
from types import MappingProxyType

@dataclass
class Command:
    """Class that represents commands"""

    command : str
    arguments : List[str]

class CommandList:
    def __init__(self,console : BotConsole):
        self._console = console
        self._commands = MappingProxyType(
            {
                "queue": (self._console.getQueue,"Prints queue of messages waiting to be posted"),
                "help" : (self._console.getCommandsList,"Prints list of all available commands"),
                "shutdown" : (self._console.shutdown,"Shutdowns the Bot"),
                "update" : (self._console.toggleUpdate,"Arguments:'start,stop'. Unlocks the updater to add new items to the message queue"),
                "posting" : (self._console.toggleMessagePosting,"Arguments:'start,stop'. Unlocks the poster to remove from the message queue"),
            }
        )

    def getCommand(self,s : str):
        if s in self._commands.keys():
            return self._commands[s]
        else:
            return -1