import sys
from pathlib import Path
from decouple import Config, RepositoryEnv


class _SettingsConfig:
    def __init__(self, envPath=None):
        self.__config = self.__loadConfig(envPath)
        self.__settingsConfig = self.__loadSettings()
        self.__role = None

    def __loadConfig(self, envPath):
        # Определяем путь в зависимости от того, сборка это или нет
        if getattr(sys, "_MEIPASS", False):
            # Если это собранный .exe, ищем .env рядом с исполняемым файлом
            basePath = Path(sys._MEIPASS)
            envFile = basePath / ".env"
        else:
            # Если это обычный скрипт, используем файл ../client/.env
            basePath = Path(__file__).resolve().parent.parent / "client"
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
            sampleLimit=self.__config("DB_LIMIT", cast=int)
        )
        __settings["LOG"] = dict(
            file=self.__config("LOG_FILE"),
            directory=self.__config("LOG_DIRECTORY")
        )
        __settings["FTP"] = dict(
            host=self.__config("FTP_HOST"),
            port=self.__config("FTP_PORT", cast=int),
            user=self.__config("FTP_USER"),
            password=self.__config("FTP_PASSWORD"),
            dir=self.__config("FTP_DIR"),
            oldVersionsDir=self.__config("FTP_OLD_VERSIONS_DIR")
        )
        return __settings

    @property
    def role(self):
        return self.__role

    @role.setter
    def role(self, role):
        self.__role = role

    @property
    def ServerSettings(self):
        return self.__settingsConfig["SERVER"]

    @property
    def DatabaseSettings(self):
        return self.__settingsConfig["DATABASE"]

    @property
    def sampleLimit(self):
        return self.DatabaseSettings["sampleLimit"]

    @property
    def LogSettings(self):
        return self.__settingsConfig["LOG"]
    
    @property
    def Ftp(self):
        return self.__settingsConfig["FTP"]

    @property
    def ftpDir(self):
        return self.Ftp["dir"]
    
    @property
    def ftpOldVersionsDir(self):
        return self.Ftp["oldVersionsDir"]


def loadSettings(envPath=None):
    return _SettingsConfig(envPath)


g_settingsConfig = loadSettings()
