import subprocess
import sys

import consts

from shared.tools.ftp import g_ftpClient
from shared.version import VersionChecker

from common.fileSystem import FileSystem
from common.logger import logger

_log = logger.getLogger(__name__)


class Updater:
    def __init__(self):
        self._ftp = None

    @classmethod
    def hello(cls):
        _log.debug("Запуск из проекта...")

    def run(self):
        _log.debug("Updater запущен...")
        self._ftp = g_ftpClient
        self._ftp.connect()
        self._ftp.init()
        self._checkVersion()
        self._ftp.disconnect()
        self._launchClient()

    def _checkVersion(self):
        _log.debug("Проверка новой версии...")
        file, remoteVersion = VersionChecker.checkVersion(
            consts.LOCAL_VERSION_FILE, 
            consts.FILE_PREFIX, 
            consts.FILE_EXTENSION,
            self._ftp
        )
        if file and remoteVersion is not None:
            _log.info(f"Найдена новая версия: {remoteVersion}. Загружаем...")
            self._installNewVersion(file)
        else:
            _log.info("Нет новой версии для загрузки.")

    def _installNewVersion(self, file):
        try:
            _log.debug("Установка новой версии...")
            self._deleteOldVersion()
            fileForUnpacking = self._downloadVersion(file)
            self._unpackingVersion(fileForUnpacking)
            self.replaceClient()
            _log.info("Установка новой версии завершена успешно.")
        except Exception as e:
            _log.error(f"Ошибка при установке новой версии: {e}", exc_info=True)

    @staticmethod
    def _deleteOldVersion():
        try:
            _log.debug("Удаление старой версии...")
            if getattr(sys, "_MEIPASS", False):
                for file in consts.FILES_FOR_DELETION:
                    FileSystem.deleteFile(file)
                _log.info("Старая версия успешно удалена.")
        except Exception as e:
            _log.error(f"Ошибка при удалении старой версии: {e}")
            return

    def _downloadVersion(self, file):
        try:
            _log.debug(f"Скачивание новой версии...")
            localPath = FileSystem.joinPaths(consts.LOCAL_DOWNLOAD_PATH, file)
            self._ftp.downloadFile(file, localPath)
            _log.info(f"Загружен файл: {localPath}")
            return localPath
        except Exception as e:
            _log.error(f"Ошибка при загрузке версии: {e}")
            return 

    @staticmethod
    def _unpackingVersion(fileForUnpacking):
        try:
            _log.debug("Распаковка новой версии...")
            FileSystem.unzip(fileForUnpacking, consts.LOCAL_DOWNLOAD_PATH)
            _log.info("Распаковка завершена успешно.")
        except Exception as e:
            _log.error(f"Ошибка при распаковке новой версии: {e}")
        finally:
            FileSystem.deleteFile(fileForUnpacking)

    @staticmethod
    def replaceClient():
        _log.debug("Замена client...")
        clientPathUnpacked = FileSystem.joinPaths(consts.LOCAL_DOWNLOAD_PATH, consts.CLIENT_EXE)
        clientPath = consts.CLIENT_PATH
        if not FileSystem.exists(clientPathUnpacked):
            _log.error(f"Файл <{clientPathUnpacked}> не найден после распаковки")
            return
        
        try:
            FileSystem.copyFile(clientPathUnpacked, clientPath, True)
            FileSystem.deleteFile(clientPathUnpacked)
        except Exception as e:
            _log.error(e)

    def _launchClient(self):
        try:
            _log.debug("Запуск client...")
            clientPath = consts.CLIENT_PATH
            if FileSystem.exists(clientPath):
                _log.info(f"Запуск {clientPath}...")
                subprocess.Popen([clientPath])
                self.close()
            else:
                _log.error(f"Файл {clientPath} не найден!")
        except Exception as e:
            _log.error(f"Ошибка при запуске client.exe: {e}")
            raise

    def close(self):
        _log.debug("Updater завершает работу.")
        sys.exit(0)
