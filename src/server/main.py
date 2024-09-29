import os
import threading

from common.logger import createLog

createLog()

from server import Server


if __name__ == "__main__":
    server = Server()
    serverThread = threading.Thread(target=server.start)
    serverThread.start()

    while True:
        user_input = input("-> ")
        if user_input == "stop":
            server.stop()
            os._exit(0)
