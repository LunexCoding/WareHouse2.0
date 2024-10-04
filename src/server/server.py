from connection import Socket

import commands.consts as consts
from commands.center import g_commandCenter

from common.logger import logger

_log = logger.getLogger(__name__)

LAUNCH_COMMANDS = [-1, -2]


class Server:
    def __init__(self):
        self._socket = None
        self._running = False

    def start(self):
        self._running = True
        for command in LAUNCH_COMMANDS:
            commandObj, data = g_commandCenter.searchCommand(command)
            if commandObj is not None:
                commandObj.execute(data)
            else:
                _log.error(consts.COMMAND_NOT_FOUND_MSG.format(command))

        self._socket = Socket(g_commandCenter)
        self._socket.start()

    def stop(self):
        self._socket.stop()
        self._running = False
