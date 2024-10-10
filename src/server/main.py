import preinit

import os
import threading

from server import Server

from common.logger import logger


logger.setLogSettings("server", filename="server.md")


if __name__ == "__main__":
    server = Server()
    serverThread = threading.Thread(target=server.start)
    serverThread.start()

    while True:
        user_input = input("-> ")
        if user_input == "stop":
            server.stop()
            os._exit(0)
