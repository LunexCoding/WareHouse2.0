from connection import Socket

import commands.consts as consts
from commands.center import g_commandCenter

from common.logger import logger

_log = logger.getLogger(__name__)

LAUNCH_COMMANDS = [-1, -2]


class Server:
    def __init__(self):
        self.socket = None
        self.running = False

    def start(self):
        self.running = True
        for command in LAUNCH_COMMANDS:
            commandObj, data = g_commandCenter.searchCommand(command)
            if commandObj is not None:
                commandObj.execute(data)
            else:
                _log.error(consts.COMMAND_NOT_FOUND_MSG.format(command))

        self.socket = Socket(g_commandCenter)
        self.socket.start()

    def stop(self):
        self.socket.stop()
        self.running = False
