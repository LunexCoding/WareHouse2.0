from commands.center import g_commandCenter, g_socket
from commands.consts import Constants
from commands.roles import Roles

from network.commands import Commands, Constants as CMDConstants
from network.status import CommandStatus

from common.logger import logger


_log = logger.getLogger(__name__)


class _User:
    def __init__(self):
        self._userID = None
        self._login = None
        self._fullname = None
        self._role = Roles.getRole(0)

    def authorization(self, login, password):
        g_socket.checkConnection()
        COMMAND_NANE = Commands.COMMAND_AUTHORIZATION.name
        commandID = Commands.getCommandByName(COMMAND_NANE, None)
        response = g_commandCenter.execute(Constants.DEFAULT_COMMAND_STRING.format(commandID, login, password))
        data = self._processingResponse(commandID, response)
        if data is None:
            _log.debug("User authorization failed.")
            return False
        self._userID = data[0]
        self._fullname = data[1]
        self._role = Roles.getRole(int(data[2]))
        _log.debug(f"User is authorized as <{self._fullname}> with UserID<{self._userID}>.")
        return True

    @staticmethod
    def _processingResponse(commandID, response):
        if response is not None:
            commandString = " ".join([item.replace(CMDConstants.SERVICE_SYMBOL, " ") for item in response]).split()
            commandIDResponse = int(commandString.pop(0))
            commandStatus = int(commandString.pop(0))
            data = commandString.copy()
            if commandID == commandIDResponse and commandStatus == CommandStatus.EXECUTED:
                return data
            return None
        return None

    @property
    def userID(self):
        return self._userID

    @property
    def login(self):
        return self._login

    @property
    def fullname(self):
        return self._fullname

    @property
    def role(self):
        return self._role


g_user = _User()
