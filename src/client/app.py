import sys
import threading
import subprocess
from pathlib import Path

import consts
from connection import g_socket

from ui.windows import MainWindow

from shared.version import VersionChecker
from shared.tools.ftp import g_ftpClient

from common.fileSystem import FileSystem
from common.logger import logger


_log = logger.getLogger(__name__)


class App:
    def __init__(self):
        self._window = None
        self._initializeUI()

    def run(self):
        try:
            
            g_ftpClient.connect()
            g_ftpClient.init()
            
            if getattr(sys, "_MEIPASS", False):
        
                file, remoteVersion = self._checkUpdaterVersion()
                if file and remoteVersion is not None:
                    _log.debug("Обновление Updater...")
                    self._downloadUpdater(file, remoteVersion)

                file, remoteVersion = self._checkClientVersion()
                if file and remoteVersion is not None:
                    _log.debug("Обновление клиента...")
                    self._runUpdater()

            else:
                from updater.updater import Updater

                Updater.hello()

            _log.debug("Запуск приложения...")
            socketThread = threading.Thread(target=self._startSocket)
            socketThread.start()
            self._runUI()

            g_ftpClient.disconnect()

        except Exception as e:
            _log.error(e, exc_info=True)

    def _initializeUI(self):
        self._window = MainWindow()
        self._window.protocol("WM_DELETE_WINDOW", self.close)

    def _runUI(self):
        self._window.mainloop()

    @staticmethod
    def _startSocket():
        try:
            _log.debug("Инициализация сокета...")
            g_socket.init()
        except Exception as e:
            _log.error("Ошибка инициализации сокета: %s", e)

    def _runUpdater(self):
        try:
            updaterExe = Path(consts.UPDATER)
            if updaterExe.exists():
                _log.debug(f"Запуск {updaterExe}...")
                process = subprocess.Popen([str(updaterExe)], close_fds=True)
                self.close()
            else:
                _log.error(f"Не удалось найти {updaterExe}")
        except Exception as e:
            _log.error(f"Ошибка при запуске Updater: {e}")

    def _checkUpdaterVersion(self):
        file, remoteVersion = VersionChecker.checkVersion(
            consts.UPDATER_LOCAL_VERSION_FILE,
            consts.UPDATER_FILE_PREFIX, 
            consts.UPDATER_FILE_EXTENSION,
            g_ftpClient
        )
        if file and remoteVersion is not None:
            _log.info(f"Найдена новая версия Updater: {remoteVersion}. Загружаем...")
            return file, remoteVersion
            
        _log.info("Нет новой версии Updater для загрузки.")
        return None, None 
    
    def _checkClientVersion(self):
        file, remoteVersion = VersionChecker.checkVersion(
            consts.CLIENT_VERSION_FILE,
            consts.CLIENT_FILE_PREFIX, 
            consts.CLIENT_FILE_EXTENSION,
            g_ftpClient
        )
        if file and remoteVersion is not None:
            _log.info(f"Найдена новая версия Client: {remoteVersion}. Загружаем...")
            return file, remoteVersion
            
        _log.info("Нет новой версии Client для загрузки.")
        return None, None 

    def _downloadUpdater(self, file, remoteVersion):
        _log.info("Загрузка новой версии Updater...")
        localPath = Path(consts.UPDATER)
        if FileSystem.exists(localPath):
            _log.info(f"Файл {localPath} уже существует, перезаписываем...")
            localPath.unlink()

        g_ftpClient.downloadFile(file, localPath)
        _log.info(f"Загружен файл: {localPath}")

        with open(consts.UPDATER_LOCAL_VERSION_FILE, "w") as file:
            file.write(str(remoteVersion))

    def close(self):
        g_ftpClient.disconnect()
        _log.debug("Приложение завершает свою работу")
        if self._window is not None:
            self._window.destroy()
        sys.exit(0)
