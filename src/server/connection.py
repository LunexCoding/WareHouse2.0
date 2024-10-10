import socket
import threading

from client import Client
from consts import RESPONSE_STRING, NOTIFICATION_STRING_RESPONSE

import commands.consts as consts

from network.commands import SERVICE_SYMBOL
from network.status import CommandStatus

from common.config import g_baseConfig
from common.logger import logger


_log = logger.getLogger(__name__, logName="server")


class Socket:
    def __init__(self, commandCenter):
        self._host = g_baseConfig.Server["host"]
        self._port = g_baseConfig.Server["port"]
        self._running = False
        self._clients = []
        self._commandCenter = commandCenter

    def handleClient(self, clientSocket, addr):
        client = Client(clientSocket, addr)
        self._clients.append(client)
        _log.debug(f"Соединение от Addr<{addr}>")

        try:
            while self._running:
                responseBuffer = ""
                request = None

                while True:
                    data = clientSocket.recv(1024).decode("utf-8")

                    if not data:
                        _log.debug(f"{client} disconnected")
                        self._clients.remove(client)
                        break

                    responseBuffer += data

                    if responseBuffer.endswith(SERVICE_SYMBOL):
                        request = responseBuffer[:-len(SERVICE_SYMBOL)]
                        break
                
                if request is not None:
                    _log.debug(f"Получено от {client}: {request}")
                    self.processCommand(client, request)
                else:
                    _log.debug(f"Нет данных для обработки от {client}")
                        
        except (ConnectionResetError, socket.error) as e:
            _log.error(f"Ошибка соединения с {client}: {e}")
            self._clients.remove(client)
        except Exception as e:
            _log.error(f"Обработка ошибок: {e}", exc_info=True)

    def processCommand(self, client, response):
        args = response.split(SERVICE_SYMBOL)
        tempCommandID, commandStr = args[0], args[1:]
        commandID = int(commandStr.pop(0))
        argsCommand = " ".join(commandStr).replace(SERVICE_SYMBOL, " ")
        commandObj, args = self._commandCenter.searchCommand(commandID)
        if commandObj is not None:
            if args is not None:
                argsCommand += args
            result = commandObj.execute(client=client, commandArgs=argsCommand)
            status, records = result[0], result[1]
            if records is not None:
                if isinstance(records, list):
                    data = "|".join(SERVICE_SYMBOL.join(map(str, record.values())) for record in records)
                else:
                    data = records
                response = RESPONSE_STRING.format(tempCommandID, commandID, status, data)
            else:
                response = RESPONSE_STRING.format(tempCommandID, commandID, status, None)
        else:
            _log.error(f"{client}: {consts.COMMAND_NOT_FOUND_MSG.format(commandID)}")
            response = RESPONSE_STRING.format(tempCommandID, commandID, CommandStatus.FAILED, consts.COMMAND_NOT_FOUND_MSG.format(commandID))
        self.sendToClient(client, response)

    def sendToClient(self, client, response):
        try:
            clientSocket = client.socket
            clientSocket.send(response.encode("utf-8"))
            _log.debug(f"Ответ {client} data: {response}")
        except socket.error as e:
            self._disconnectClient(client)

    def sendNotifications(self, notificationType, args):
        args = SERVICE_SYMBOL.join(args)
        notification = NOTIFICATION_STRING_RESPONSE.format(notificationType, args)

        for client in self._clients:
            try:
                self.sendToClient(client, notification)
                _log.debug(f"Уведомление: {notification} отправлено клиенту <{client}>")
            except socket.error as e:
                _log.error(f"Ошибка отправки уведомления: {e}")

    def start(self):
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSocket.bind((self._host, self._port))
        serverSocket.listen(5)
        self._running = True
        _log.debug(f"Server listening on {self._host}:{self._port}")

        while self._running:
            try:
                clientSocket, addr = serverSocket.accept()
                threading.Thread(target=self.handleClient, args=(clientSocket, addr), daemon=True).start()
            except Exception as e:
                _log.error(f"Ошибка принятия клиента: {e}")

    def stop(self):
        _log.debug("Остановка сокета...")
        self._running = False
        for client in self._clients:
            client.socket.shutdown(socket.SHUT_RDWR)
            self._disconnectClient(client)
        _log.debug("Сокет остановлен.")

    def _disconnectClient(self, client):
        try:
            client.socket.close()
            self._client.remove(client)
            _log.debug(f"Клиент <{client}> отключен")
        except Exception as e:
            _log.error(f"Не удалось отключить {client}: {e}")
