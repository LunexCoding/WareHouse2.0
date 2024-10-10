from commands.localCommands import UpdateFile

from network.notifications import CommandType


class CommandFactory:
    _COMMANDS = {
        CommandType.UPDATE_FILE: UpdateFile,
    }

    @classmethod
    def getCommand(cls, commandID):
        try:
            commandType = CommandType(int(commandID))
        except ValueError:
            return None
        
        return cls._COMMANDS.get(commandType)()
