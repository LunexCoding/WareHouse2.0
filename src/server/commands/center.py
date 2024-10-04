from .consts import Commands
from .client import COMMANDS as clientCommands
from .service import COMMANDS as serviceCommands


class CommandCenter:
    def __init__(self):
        self.commands = {**serviceCommands, **clientCommands}

    def searchCommand(self, commandID):
        commandData = Commands.getCommandByID(commandID)
        command = self.commands.get(commandData.name, None)
        if command is None:
            return None
        params = self.updateCommandParams(commandData.params)

        return command(), params

    def updateCommandParams(self, params):
        if params is None:
            return None
        
        if isinstance(params, dict):
            table = params.get("table", None)
            if table is None:
                return None
            return f" -t {table}"
        return None


g_commandCenter = CommandCenter()
