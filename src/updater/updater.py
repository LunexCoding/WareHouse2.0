import subprocess
import sys

import consts

from shared.version import VersionChecker

from common.config import g_baseConfig
from common.ftp import g_ftp
from common.fileSystem import FileSystem
from common.logger import logger

_log = logger.getLogger(__name__, "updater")


class Updater:
    def __init__(self):
        self._ftp = None

    @classmethod
    def hello(cls):
        _log.debug("Запуск из проекта...")

    def run(self):
        _log.debug("Updater запущен...")
        g_ftp.connect()
        self._checkVersion()
        self.updateFiles()
        g_ftp.disconnect()
        self._launchClient()

    def close(self):
        _log.debug("Updater завершает работу.")
        sys.exit(0)

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

    @staticmethod
    def updateFiles():
        for file in g_baseConfig.FilesForUpdate:
            localTime = FileSystem.getModificationTime(file)
            remoteTime = g_ftp.getModificatioTime(file)
            if FileSystem.compareTimestamps(remoteTime, localTime):
                _log.debug(f"Обновление: {file}")
                g_ftp.downloadFile(file, file)

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
