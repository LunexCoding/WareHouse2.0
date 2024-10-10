import sys
from pathlib import Path
from decouple import Config, RepositoryEnv


class _BaseConfig:
    def __init__(self, envPath=None):
        self.__config = self.__loadConfig(envPath)
        self.__settingsConfig = self.__loadSettings()

    def __loadConfig(self, envPath):
        # Определяем путь в зависимости от того, сборка это или нет
        if getattr(sys, "_MEIPASS", False):
            # Если это собранный .exe, ищем .env рядом с исполняемым файлом
            basePath = Path(sys._MEIPASS)
            envFile = basePath / ".env"
        else:
            # Если это обычный скрипт, используем файл ../client/.env
            basePath = Path(__file__).resolve().parent.parent / "common"
            envFile = basePath / ".env"

        # Если путь к .env указан вручную, то используем его
        if envPath:
            envFile = Path(envPath)

        if not envFile.exists():
            raise FileNotFoundError(f".env file not found at: {envFile}")

        return Config(RepositoryEnv(envFile))
    
    def __loadSettings(self):
        __settings = {}
        __settings["SERVER"] = dict(
            host=self.__config("SERVER_HOST"),
            port=self.__config("SERVER_PORT", cast=int)
        )
        __settings["DATABASE"] = dict(
            limit=self.__config("DB_LIMIT", cast=int)
        )
        __settings["FTP"] = dict(
            host=self.__config("FTP_HOST"),
            port=self.__config("FTP_PORT", cast=int),
            user=self.__config("FTP_USER"),
            password=self.__config("FTP_PASS"),
            root=self.__config("FTP_ROOT")
        )
        __settings["FTP"]["dirs"] = dict(
            root=__settings["FTP"]["root"],
            oldVersions=self.__config("FTP_OLD_VERSIONS_DIR"),
            oldClients=self.__config("FTP_OLD_VERSIONS_CLIENT_DIR"),
            oldServers=self.__config("FTP_OLD_VERSIONS_SERVER_DIR"),
            oldUpdaters=self.__config("FTP_OLD_VERSIONS_UPDATER_DIR"),
            data=self.__config("FTP_DATA_DIR"),
            reports=self.__config("FTP_REPORTS_DIR")
        )
        __settings["DATA"] = dict(
            dir=Path(self.__config("DATA_DIR")),
            reportsDir=self.__config("REPORT_DIR"),
            pricesFile=self.__config("PRICES_FILE"),
        )
        __settings["DIRECTORIES"] = [
            __settings["DATA"]["dir"],
            __settings["DATA"]["reportsDir"]
        ]
        __settings["FILES_UPDATE"] = [
            __settings["DATA"]["pricesFile"]
        ]
        return __settings

    @property
    def Server(self):
        return self.__settingsConfig["SERVER"]

    @property
    def Database(self):
        return self.__settingsConfig["DATABASE"]

    @property
    def Ftp(self):
        return self.__settingsConfig["FTP"]
    
    @property
    def FtpDirs(self):
        return self.__settingsConfig["FTP"]["dirs"]
    
    @property
    def Data(self):
        return self.__settingsConfig["DATA"]
    
    @property
    def Dirs(self):
        return self.__settingsConfig["DIRECTORIES"]

    @property
    def FilesForUpdate(self):
        return self.__settingsConfig["FILES_UPDATE"]


def loadSettings(envPath=None):
    return _BaseConfig(envPath)


g_baseConfig = loadSettings()
