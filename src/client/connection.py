import socket

import consts

from shared.config import g_settingsConfig

from common.logger import logger

_log = logger.getLogger(__name__)


class _Socket:
    def __init__(self, host, port):
        self._host = host
        self._port = port
        self._clientSocket = None
        self._responses = []

    def init(self):
        if not self.checkConnection():
            logger.getLogger(__name__).debug(f"Failed to connect to server {self._host}:{self._port}")
        else:
            _log.debug(f"Successfully connected to server {self._host}:{self._port}")

    def connect(self):
        self._clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._clientSocket.connect((self._host, self._port))
        _log.debug(f"Connected to server {self._host}:{self._port}")

    def sendCommand(self, command):
        if not self.checkConnection():
            _log.error(consts.CLIENT_IS_NOT_CONNECTED_MSG)
            raise ConnectionError(consts.CLIENT_IS_NOT_CONNECTED_MSG)
        self._clientSocket.sendall(str(command).encode("utf-8"))
        _log.debug(consts.SENT_MSG.format(command))

    def receiveResponse(self):
        if not self.checkConnection():
            _log.error(consts.CLIENT_IS_NOT_CONNECTED_MSG)
            raise ConnectionError(consts.CLIENT_IS_NOT_CONNECTED_MSG)
        receivedData = ""
        while True:
            response = self._clientSocket.recv(1024).decode("utf-8")
            if response[-1] != " ":
                receivedData += response
                break
            receivedData += response
        return receivedData

    def sendAndReceiveSync(self, command):
        self.sendCommand(command)
        response = self.receiveResponse()
        _log.debug(consts.RECEIVED_MSG.format(response))
        return response.split()

    def sendAndReceiveAsync(self, commands):
        self.clearResponses()
        try:
            for command in commands:
                response = self.sendAndReceiveSync(command)
                self._responses.append(response)
            if len(commands) == 1:
                return self._responses[0]
            return self._responses
        except OSError as e:
            _log.error(e)
            return None

    def clearResponses(self):
        self._responses.clear()

    def checkConnection(self):
        try:
            if self._clientSocket is None:
                self.connect()  # Создаем и подключаем сокет
            else:
                self._clientSocket.settimeout(1)
                self._clientSocket.send(b'')  # Проверяем, активен ли сокет
            return True
        except (socket.timeout, socket.error):
            _log.debug("Проверка подключения сокета провалена")
            return False
        finally:
            # Возвращаем стандартный таймаут
            if self._clientSocket:
                self._clientSocket.settimeout(10)

    def close(self):
        if self._clientSocket:
            self._clientSocket.close()
            _log.debug("Socket closed")

g_socket = _Socket(
    g_settingsConfig.ServerSettings["host"],
    g_settingsConfig.ServerSettings["port"]
)
