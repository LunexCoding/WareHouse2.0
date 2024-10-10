import sys
import threading
import subprocess
from pathlib import Path

import consts
from connection import g_socket

from commands.localCommands import UpdateFile

from ui.windows import MainWindow

from shared.version import VersionChecker

from notifications.notification import NotificationFactory

from common.config import g_baseConfig
from common.ftp import g_ftp
from common.fileSystem import FileSystem
from common.logger import logger


_log = logger.getLogger(__name__, "app")


class App:
    def __init__(self):
        self._window = None
        self._initializeUI()

        g_socket.setNotificationHandler(self._handleNotification)

    def run(self):
        try:
            self._initDirs()
            g_ftp.connect()
            
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
                Updater.updateFiles()

            _log.debug("Запуск приложения...")
            
            socketThread = threading.Thread(target=self._startSocket)
            socketThread.start()

            self._runUI()

        except Exception as e:
            _log.error(e, exc_info=True)

    def close(self):
        g_ftp.disconnect()
        _log.debug("Приложение завершает свою работу")
        if self._window is not None:
            self._window.destroy()
        sys.exit(0)

    @staticmethod
    def _initDirs():
        for dir in g_baseConfig.Dirs:
            FileSystem.makeDir(dir, True)

    def _initializeUI(self):
        self._window = MainWindow()
        self._window.protocol("WM_DELETE_WINDOW", self.close)

    def _runUI(self):
        self._window.mainloop()

    @staticmethod
    def _startSocket():
        try:
            _log.debug("Инициализация сокета...")
            g_socket.start()
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
            g_ftp
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
            g_ftp
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

        g_ftp.downloadFile(file, localPath)
        _log.info(f"Загружен файл: {localPath}")

        with open(consts.UPDATER_LOCAL_VERSION_FILE, "w") as file:
            file.write(str(remoteVersion))

    def _handleNotification(self, notification):
        _log.debug(f"Уведомление: {notification}")
        data = notification.split(" ")
        notificationType, notificationData = data[0], data[1:]
        
        notificationClass = NotificationFactory.getNotificationClass(notificationType)
        if notificationClass:
            notificationClass(notificationData).handle(self)
        else:
            _log.debug(f"Неизвестное уведомление: {notification}")
            self._window.showNotification(notification)
