import os
import threading

import preinit

preinit.createLog()

from connection import Socket
from commands.center import g_commandCenter
from commands.consts import Constants

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
                _log.error(Constants.COMMAND_NOT_FOUND_MSG.format(command))

        self.socket = Socket(g_commandCenter)
        self.socket.start()

    def stop(self):
        self.socket.stop()
        self.running = False


if __name__ == "__main__":
    server = Server()
    server_thread = threading.Thread(target=server.start)
    server_thread.start()

    while True:
        user_input = input("-> ")
        if user_input == "stop":
            server.stop()
            os._exit(0)
