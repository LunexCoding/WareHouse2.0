from collections import namedtuple

from network.tables import DatabaseTables


SERVICE_SYMBOL = "\0"
SERVICE_SYMBOL_FOR_ARGS = "&"
COMMAND_AUTHORIZATION = "auth"
COMMAND_SEARCH = "search"
COMMAND_LOAD = "load"
COMMAND_ADD = "add"
COMMAND_DELETE = "del"
COMMAND_UPDATE = "upd"


COMMAND = namedtuple("Command", ["id", "name", "params"])


class Commands:
    COMMAND_AUTHORIZATION = COMMAND(0, COMMAND_AUTHORIZATION, None)
    COMMAND_LOAD_USERS = COMMAND(1, COMMAND_LOAD, dict(table=DatabaseTables.USERS))
    COMMAND_SEARCH_USERS = COMMAND(2, COMMAND_SEARCH, dict(table=DatabaseTables.USERS))
    COMMAND_ADD_USER = COMMAND(3, COMMAND_ADD, dict(table=DatabaseTables.USERS))
    COMMAND_DELETE_USER = COMMAND(4, COMMAND_DELETE, dict(table=DatabaseTables.USERS))
    COMMAND_UPDATE_USER = COMMAND(5, COMMAND_UPDATE, dict(table=DatabaseTables.USERS))

    @classmethod
    def getCommandByName(cls, name, params):
        for command in cls.__dict__.values():
            if isinstance(command, COMMAND) and command.name == name and command.params == params:
                return command.id
        return None

    @classmethod
    def getCommandByID(cls, commandID):
        for command in cls.__dict__.values():
            if isinstance(command, COMMAND) and command.id == commandID:
                return command
        return None
