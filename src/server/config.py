from pathlib import Path

from decouple import config


class _SettingsConfig:
    def __init__(self):
        self.__settingsConfigDB = self.__loadSettingsDB()

    def __loadSettingsDB(self):
        __settings = {}
        __settings["SERVER"] = dict(
            host=config("SERVER_HOST"),
            port=config("SERVER_PORT", cast=int)
        )
        __settings["DATABASE"] = dict(
            database=config("DB_NAME"),
            databaseDirectory=config("DB_DIRECTORY"),
            fullPath=Path(config("DB_DIRECTORY")) / config("DB_NAME"),
            sampleLimit=config("DB_LIMIT")
        )
        return __settings

    @property
    def ServerSettings(self):
        return self.__settingsConfigDB["SERVER"]

    @property
    def DatabaseSettings(self):
        return self.__settingsConfigDB["DATABASE"]


g_settingsConfig = _SettingsConfig()
