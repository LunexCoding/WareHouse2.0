import socket
import threading

from client import Client
from config import g_settingsConfig
from consts import RESPONSE_STRING

import commands.consts as consts

from network.commands import SERVICE_SYMBOL
from network.status import CommandStatus

from common.logger import logger

_log = logger.getLogger(__name__)


class Socket:
    def __init__(self, commandCenter):
        self.host = g_settingsConfig.ServerSettings["host"]
        self.port = g_settingsConfig.ServerSettings["port"]
        self.running = False
        self.clients = []
        self.commandCenter = commandCenter

    def handleClient(self, clientSocket, addr):
        client = Client(clientSocket, addr)
        self.clients.append(client)
        _log.debug(f"Соединение от Addr<{addr}>")

        try:
            while self.running:
                responseBuffer = ""
                request = None

                while True:
                    data = clientSocket.recv(1024).decode("utf-8")

                    if not data:
                        _log.debug(f"{client} disconnected")
                        self.clients.remove(client)
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
        except Exception as e:
            _log.error(f"Обработка ошибок: {e}", exc_info=True)

    def processCommand(self, client, response):
        args = response.split(SERVICE_SYMBOL)
        tempCommandID, commandStr = args[0], args[1:]
        commandID = int(commandStr.pop(0))
        argsCommand = " ".join(commandStr).replace(SERVICE_SYMBOL, " ")
        commandObj, args = self.commandCenter.searchCommand(commandID)
        if commandObj is not None:
            if args is not None:
                argsCommand += args
            result = commandObj.execute(client, argsCommand)
            status, records = result[0], result[1]
            if records is not None:
                if isinstance(records, list):
                    data = "|".join(SERVICE_SYMBOL.join(map(str, record.values())) for record in records)
                else:
                    data = records
                response = RESPONSE_STRING.format(tempCommandID, commandID, status, data)
            else:
                data = None
                response = RESPONSE_STRING.format(tempCommandID, commandID, status, data)
        else:
            _log.error(f"{client}: {consts.COMMAND_NOT_FOUND_MSG.format(commandID)}")
            response = RESPONSE_STRING.format(tempCommandID, commandID, CommandStatus.FAILED, consts.COMMAND_NOT_FOUND_MSG.format(commandID))
        self.sendToClient(client, response)

    @staticmethod
    def sendToClient(client, response):
        clientSocket = client.socket
        clientSocket.send(response.encode("utf-8"))
        _log.debug(f"Ответ {client} data: {response}")

    def start(self):
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSocket.bind((self.host, self.port))
        serverSocket.listen(5)
        self.running = True
        _log.debug(f"Server listening on {self.host}:{self.port}")

        while self.running:
            try:
                clientSocket, addr = serverSocket.accept()
                threading.Thread(target=self.handleClient, args=(clientSocket, addr)).start()
            except Exception as e:
                _log.error(f"Ошибка принятия клиента: {e}")

    def stop(self):
        _log.debug("Остановка сокета...")
        self.running = False
        for client in self.clients:
            try:
                client.socket.shutdown(socket.SHUT_RDWR)
                client.socket.close()
            except Exception as e:
                _log.error(f"Не удалось отключить {client}: {e}")

        self.clients.clear()
        _log.debug("Сокет остановлен.")
