from pathlib import Path

from decouple import config

from common.config import g_baseConfig


class _SettingsConfig:
    def __init__(self):
        self.__settingsConfig = self.__loadSettingsDB()

    def __loadSettingsDB(self):
        __settings = {}
        __settings["DATA"] = dict(
            driversDir=g_baseConfig.Data["dir"] / config("DRIVERS_DIRECTORY")
        )
        __settings["DATABASE"] = dict(
            database=config("DB_NAME"),
            databaseDirectory=g_baseConfig.Data["dir"],
            fullPath=g_baseConfig.Data["dir"] / config("DB_NAME")
        )
        __settings["PARSER"] = dict(
            url=config("PARSER_URL")
        )
        __settings["DIRECTORIES"] = g_baseConfig.Dirs + [
            __settings["DATA"]["driversDir"]
        ]
        return __settings

    @property
    def DataSettings(self):
        return self.__settingsConfig["DATA"]

    @property
    def DatabaseSettings(self):
        return self.__settingsConfig["DATABASE"]
    
    @property
    def ParserSettings(self):
        return self.__settingsConfig["PARSER"]
    
    @property
    def Directories(self):
        return self.__settingsConfig["DIRECTORIES"]


g_settingsConfig = _SettingsConfig()
