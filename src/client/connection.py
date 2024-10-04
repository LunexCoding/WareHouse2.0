import socket
import threading
import queue

import consts

from shared.config import g_settingsConfig

from network.commands import SERVICE_SYMBOL, NOTIFICATION_COMMAND_ID

from common.logger import logger

_log = logger.getLogger(__name__)


class _Socket:
    def __init__(self, host='localhost', port=9999):
        self._host = host
        self._port = port
        self._socket = None
        self._receiveThread = None
        self._running = False
        self._commandID = 1
        self._lastCommandID = None
        self._responses = queue.Queue()

    def start(self):
        try:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.connect((self._host, self._port))
            _log.debug(f"Подключен к серверу {self._host}:{self._port}")
        except socket.error as e:
            _log.error(f"Ошибка подключения: {e}")
            return

        self._running = True

        self._receiveThread = threading.Thread(target=self.receive, daemon=True)
        self._receiveThread.start()

    def close(self):
        self._running = False
        if self._socket is not None:
            self._socket.close()

    def reconnect(self):
        _log.debug("Reconnecting...")
        if self._socket is not None:
            self._socket.close()
        self.connect()

    def checkConnection(self, attempts=3):
        if self._socket is None:
            _log.debug("Socket отсутствует, попытка подключения...")
            self.connect()
        try:
            self._socket.send(b'')
            return True
        except (socket.timeout, socket.error):
            if attempts > 0:
                _log.debug("Проверка подключения сокета не удалась, повторное подключение...")
                self.reconnect()
                return self.checkConnection(attempts - 1)
            else:
                _log.debug("Достигнуто максимальное количество попыток подключения.")
                return False

    def send(self, command):
        if not self.checkConnection():
            _log.error(consts.CLIENT_IS_NOT_CONNECTED_MSG)
            return None

        try:
            commandStr = f"{self._commandID}{SERVICE_SYMBOL}{command}{SERVICE_SYMBOL}"
            self._socket.send(commandStr.encode('utf-8'))
            self._lastCommandID = self._commandID
            self._commandID += 1
            _log.debug(consts.SENT_MSG.format(self._lastCommandID, commandStr))
            return self._responses.get()
        except socket.error as e:
            _log.error(f"Ошибка отправки команды: {e}")
            return None

    def receive(self):
        while self._running:
            try:
                responseBuffer = ""
                while True:
                    response = self._socket.recv(1024).decode("utf-8")

                    if not response:
                        break
                    responseBuffer += response

                    if responseBuffer.endswith(SERVICE_SYMBOL):
                        responseBuffer = responseBuffer[:-len(SERVICE_SYMBOL)]
                        break
                
                _log.debug(f"Ответ: {responseBuffer}")
                self._processingResponse(responseBuffer)

            except socket.timeout:
                continue
            except (ConnectionResetError, socket.error):
                _log.error("Соединение разорвано.")
                break

    def _processingResponse(self, response):
        args = response.split(SERVICE_SYMBOL)
        commandID, commandStr = int(args[0]), args[1:]

        if commandID == self._lastCommandID:
            self._responses.put(commandStr)
        else:
            if commandID == NOTIFICATION_COMMAND_ID:
                _log.debug(f"Уведомление: {commandStr}")
            else:
                _log.debug(f"Неизвестный ответ: {args}")
    
        
g_socket = _Socket(
    g_settingsConfig.ServerSettings["host"],
    g_settingsConfig.ServerSettings["port"]
)
