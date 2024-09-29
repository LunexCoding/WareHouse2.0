import argparse
import ftplib
import os
from packaging.version import Version, InvalidVersion
import re

from shared.config import g_settingsConfig

from common.logger import logger

try:
    _log = logger.getLogger("ftp")
except TypeError:
    logger.createLog(g_settingsConfig.LogSettings["directory"], g_settingsConfig.LogSettings["file"])
    _log = logger.getLogger("ftp")


class _FTPClient:
    def __init__(self, username, password, server, port, dir):
        self._server = server
        self._port = port
        self._username = username
        self._password = password
        self._ftp = None
        self._dir = dir
    
    def connect(self):
        try:
            self._ftp = ftplib.FTP()
            self._ftp.connect(self._server, self._port)
            self._ftp.login(self._username, self._password)
            _log.debug(f"Подключен к FTP")
        except ftplib.all_errors as e:
            self._ftp = None
            _log.error(f"Ошибка подключения: {e}")
    
    def disconnect(self):
        if self._ftp is not None:
            self._ftp.quit()
            _log.debug("Отключение от FTP")
        else:
            _log.debug("FTP соединение уже закрыто или не было установлено")
    
    def init(self):
        self.initializeDirectories(
                [
                    f"{self._dir}/{g_settingsConfig.ftpOldVersionsDir}",
                    f"{self._dir}/{g_settingsConfig.ftpOldVersionsDir}/updater",
                    f"{self._dir}/{g_settingsConfig.ftpOldVersionsDir}/client",
                    f"{self._dir}/{g_settingsConfig.ftpOldVersionsDir}/server",
                ]
            )
        
    def initializeDirectories(self, directories):
        for directory in directories:
            try:
                self._ftp.mkd(directory)  # Создание папки
                _log.debug(f"Создана папка <{directory}>")
            except ftplib.error_perm as e:
                _log.debug(f"Папка уже существует <{directory}>")
    
    def uploadFile(self, localFilePath, remoteFilePath):
        remoteFilePath = self._getFullRemotePath(remoteFilePath)
        if not os.path.exists(localFilePath):
            _log.error(f"Файл не найден: {localFilePath}")
            return False
        try:
            with open(localFilePath, "rb") as file:
                self._ftp.storbinary(f"STOR {remoteFilePath}", file)
            _log.debug(f"Загружен {localFilePath} to {remoteFilePath}")
            return True
        except ftplib.all_errors as e:
            _log.error(f"Ошибка загрузки: {e}")
            return False
    
    def downloadFile(self, remoteFilePath, localFilePath):
        remoteFilePath = self._getFullRemotePath(remoteFilePath)
        try:
            with open(localFilePath, "wb") as file:
                self._ftp.retrbinary(f"RETR {remoteFilePath}", file.write)
            _log.debug(f"Скачан {remoteFilePath} to {localFilePath}")
            return True
        except ftplib.all_errors as e:
            _log.error(f"Ошибка скачивания {remoteFilePath}: {e}")
            return False

    def fileExists(self, remoteFilePath):
        remoteFilePath = self._getFullRemotePath(remoteFilePath)
        try:
            directory, file_name = os.path.split(remoteFilePath)
            files = self._ftp.nlst(directory)
            if file_name in files:
                _log.debug(f"Файл существует: {remoteFilePath}")
                return True
            else:
                _log.debug(f"Файл не сущетсвует: {remoteFilePath}")
                return False
        except ftplib.error_perm as e:
            if str(e).startswith("550"):
                _log.debug(f"Файл не найден (550): {remoteFilePath}")
                return False
            else:
                _log.error(f"Ошибка FTP: {e}")
                return False
        except ftplib.all_errors as e:
            _log.error(f"Ошибка при проверке существования файла: {e}")
            return False
        
    def findVersionedFile(self, prefix, extension):
        try:
            files = self._ftp.nlst(self._dir)
            versionPattern = re.compile(rf"{prefix}(\d+\.\d+\.\d+)\.{extension}$")
            for file in files:
                match = versionPattern.match(file)
                if match:
                    versionStr = match.group(1)
                    try:
                        version = Version(versionStr)
                        _log.debug(f"Найден версионный файл: <{file}> с версией <{version}>")
                        return file, version
                    except InvalidVersion:
                        _log.error(f"Невалидный формат версии в файле: <{file}>")
            _log.debug(f"Не найден версионный файл с префиксом: <{prefix}> и расширением: <{extension}>")
            return None, None
        except ftplib.all_errors as e:
            _log.error(f"Ошибка при получении списка файлов с FTP: {e}")
            return None, None

    def listDir(self, directory=None):
        previousDir = self._ftp.pwd()
        try:
            if directory:
                self._ftp.cwd(directory)
            files = self._ftp.nlst()
            return files
        except ftplib.all_errors as e:
            _log.error(f"Ошибка при выводе списка файлов на FTP: {e}")
            return []
        finally:
            self._ftp.cwd(previousDir)

    def uploadBuildFile(self, file):
        filename = os.path.basename(file)
        baseFilename = filename.split("_")[0]
        oldVersionDir = self._getFullRemotePath(g_settingsConfig.ftpOldVersionsDir)

        if baseFilename in ["client", "updater", "server"]:
            oldVersionSubdir = f"{oldVersionDir}/{baseFilename}"
        else:
            oldVersionSubdir = oldVersionDir

        try:
            existingFile = next((f for f in self.listDir(self._dir) if f.startswith(baseFilename)), None)
            if existingFile:
                _log.debug(f'Найден существующий файл: <{existingFile}>. Перемещение в <{oldVersionSubdir}>')
                self._ftp.rename(self._getFullRemotePath(existingFile), f"{oldVersionSubdir}/{existingFile}")

            success = self.uploadFile(file, filename)
            if success:
                _log.debug(f"Файл <{filename}> успешно загружен на FTP сервер")
            return success

        except Exception as e:
            _log.error(f"Ошибка при загрузке файла на FTP: {e}", exc_info=True)
            return False

    def _getFullRemotePath(self, remotePath):
        path = os.path.join(self._dir, remotePath)
        return path.replace("\\", "/")

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, excType, excValue, trace):
        self.disconnect()
        return False
    
    @property
    def ftp(self):
        return self._ftp
    
    
g_ftpClient = _FTPClient(
    username=g_settingsConfig.Ftp["user"],
    password=g_settingsConfig.Ftp["password"],
    server=g_settingsConfig.Ftp["host"],
    port=g_settingsConfig.Ftp["port"],
    dir=g_settingsConfig.Ftp["dir"]
)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Загрузка архива на FTP сервер.")
    parser.add_argument('--file', required=True, help="Путь к файлу для загрузки")

    args = parser.parse_args()
    filePath = args.file

    if not os.path.exists(filePath):
        _log.error(f"Файл <{filePath}> не найден.")
        exit(1)

    with g_ftpClient as ftp:
        ftp.init()
        success = ftp.uploadBuildFile(filePath)

    if not success:
        exit(1)
