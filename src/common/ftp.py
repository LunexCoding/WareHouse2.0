import argparse
import os
from packaging.version import Version, InvalidVersion
import re
import ftplib
from datetime import datetime

from common.config import g_baseConfig
from common.logger import logger


_log = logger.getLogger(__name__, "ftp")


class _Ftp:
    def __init__(self, host, port, username, password, root):
        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self._root = root
        self._ftp = None

    def connect(self):
        try:
            self._ftp = ftplib.FTP()
            self._ftp.connect(self._host, self._port)
            self._ftp.login(self._username, self._password)
            _log.debug(f"Подключен к FTP")
        except ftplib.all_errors as e:
            self._ftp = None
            _log.error(f"Ошибка подключения: {e}")
    
    def disconnect(self):
        if self._ftp is not None:
            self._ftp.quit()
            _log.debug("Отключение FTP")
        else:
            _log.debug("Соединение с FTP уже закрыто или не было установлено")
        
    def initializeDirectories(self):
        for directory in list(g_baseConfig.FtpDirs.values()):
            try:
                self._ftp.mkd(directory)
                _log.debug(f"Создана папка <{directory}>")
            except ftplib.error_perm as e:
                _log.debug(f"Папка уже существует <{directory}>")

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
    
    def uploadFile(self, localFilePath, remoteFilePath):
        remoteFilePath = self._getFullRemotePath(remoteFilePath)
        if not os.path.exists(localFilePath):
            _log.error(f"Локадьный файл не найден: {localFilePath}")
            return False
        try:
            _log.debug(f"Выгрузка <{remoteFilePath}>...")
            with open(localFilePath, "rb") as file:
                self._ftp.storbinary(f"STOR {remoteFilePath}", file)
            _log.debug(f"Выгрузен {localFilePath} to {remoteFilePath}")
            return True
        except ftplib.all_errors as e:
            _log.error(f"Ошибка выгрузки {localFilePath} to {remoteFilePath}: {e}")
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
            files = self.listDir(self._root)
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

    def listDir(self, directory):
        previousDir = self._ftp.pwd()
        try:
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
        oldVersionDir = g_baseConfig.FtpDirs["oldVersions"]

        if baseFilename in ["client", "updater", "server"]:
            oldVersionSubdir = f"{oldVersionDir}/{baseFilename}"
        else:
            oldVersionSubdir = oldVersionDir

        try:
            existingFile = next((f for f in self.listDir(self._root) if f.startswith(baseFilename)), None)
            if existingFile:
                fullNewPath = f"{oldVersionSubdir}/{existingFile}"
                fullExistingFilePath = self._getFullRemotePath(existingFile)
                
                _log.debug(f"Найден существующий файл: <{fullExistingFilePath}>. Перемещение в <{fullNewPath}>")
                self._ftp.rename(fullExistingFilePath, fullNewPath)
                _log.debug(f"Файл <{fullExistingFilePath}> перемещен в <{fullNewPath}>")

            return self.uploadFile(file, filename)

        except ftplib.error_perm as e:
            _log.debug(f"Perm: {e}")

        except Exception as e:
            _log.error(f"Ошибка при выгрузке файла на FTP: {e}", exc_info=True)
            return False

    def getModificatioTime(self, filePath):
        fullPath = self._getFullRemotePath(filePath)
        try:
            modifiedTime = self._ftp.sendcmd(f"MDTM {fullPath}")
            modifiedTime = modifiedTime[4:]
            dt = datetime.strptime(modifiedTime, "%Y%m%d%H%M%S")
            return dt
        except:
            _log.debug(f"Файл не найден: {fullPath}")
            return None

    def _getFullRemotePath(self, remotePath):
        return f"{self._root}/{remotePath}"

    @property
    def ftp(self):
        return self._ftp

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, excType, excValue, trace):
        self.disconnect()
        return False
    
    
g_ftp = _Ftp(
    host=g_baseConfig.Ftp["host"],
    port=g_baseConfig.Ftp["port"],
    username=g_baseConfig.Ftp["user"],
    password=g_baseConfig.Ftp["password"],
    root=g_baseConfig.Ftp["root"]
)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Загрузка архива на FTP сервер.")
    parser.add_argument('--file', required=True, help="Путь к файлу для загрузки")

    args = parser.parse_args()
    filePath = args.file

    if not os.path.exists(filePath):
        _log.error(f"Файл <{filePath}> не найден.")
        exit(1)

    with g_ftp as ftp:
        ftp.initializeDirectories()
        success = ftp.uploadBuildFile(filePath)

        if not success:
            exit(1)
