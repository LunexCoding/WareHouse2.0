import threading

from apscheduler.schedulers.background import BackgroundScheduler

from config import g_settingsConfig
from connection import Socket

import commands.consts as consts
from commands.center import g_commandCenter

from network.status import CommandStatus

from common.ftp import g_ftp
from common.fileSystem import FileSystem
from common.logger import logger


_log = logger.getLogger(__name__, logName="server")

LAUNCH_COMMANDS = [-1, -2]


class Server:
    def __init__(self):
        self._socket = None
        self._running = False
        self._socketThread = None
        self._scheduler = BackgroundScheduler()

    def start(self):
        self._running = True
        self._initDirs()
        g_ftp.connect()
        g_ftp.initializeDirectories()

        results = self._runStartupCommands()
        if all([result == CommandStatus.EXECUTED for result in results]):
            _log.error("Стартовые команды не выполнены")
            raise 

        self._socket = Socket(g_commandCenter)
        socketThread = threading.Thread(target=self._socket.start, daemon=True)
        socketThread.start()

        parserCommand, data = g_commandCenter.searchCommand(-3)
        self._scheduler.add_job(
            parserCommand.execute,
            kwargs={'socket': self._socket},
            trigger='interval', 
            minutes=1
        )

        self._scheduler.start()

    def stop(self):
        self._scheduler.shutdown()
        g_ftp.disconnect()

        if self._socket:
            self._socket.stop()
        if self._socketThread and self._socketThread.is_alive():
            self._socketThread.join()

        self._running = False

    @staticmethod
    def _initDirs():
        for dir in g_settingsConfig.Directories:
            FileSystem.makeDir(dir, True)

    @staticmethod
    def _runStartupCommands():
        results = []
        for command in LAUNCH_COMMANDS:
            commandObj, data = g_commandCenter.searchCommand(command)
            if commandObj is None:
                _log.error(consts.COMMAND_NOT_FOUND_MSG.format(command))
                results.append(CommandStatus.FAILED)
            try:
                if data is None:
                    results.append(commandObj.execute()[0])
                else:
                    results.append(commandObj.execute(data)[0])
            except Exception as e:
                _log.error(f"Ошибка при выполнении команды <{commandObj.COMMAND_NAME}>: {e}", exc_info=True)
                results.append(CommandStatus.FAILED)
                
        return results