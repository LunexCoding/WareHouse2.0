from pathlib import Path

from decouple import config


class _SettingsConfig:
    def __init__(self):
        self.__settingsConfigDB = self.__loadSettingsDB()

    def __loadSettingsDB(self):
        __settings = {}
        __settings["DATA"] = dict(
            directory=Path(config("DATA_DIRECTORY")),
            pricesFile=Path(config("DATA_DIRECTORY")) / config("PRICES_FILE"),
            reportDir=Path(config("REPORT_DIRECTORY"))
        )
        __settings["SERVER"] = dict(
            host=config("SERVER_HOST"),
            port=config("SERVER_PORT", cast=int)
        )
        __settings["DATABASE"] = dict(
            database=config("DB_NAME"),
            databaseDirectory=__settings["DATA"]["directory"],
            fullPath=__settings["DATA"]["directory"] / config("DB_NAME"),
            sampleLimit=config("DB_LIMIT")
        )
        __settings["PARSER"] = dict(
            url=config("PARSER_URL")
        )
        __settings["DIRECTORIES"] = [
            __settings["DATA"]["directory"],
            __settings["DATA"]["reportDir"]
        ]
        return __settings

    @property
    def DataSettings(self):
        return self.__settingsConfigDB["DATA"]

    @property
    def ServerSettings(self):
        return self.__settingsConfigDB["SERVER"]

    @property
    def DatabaseSettings(self):
        return self.__settingsConfigDB["DATABASE"]
    
    @property
    def ParserSettings(self):
        return self.__settingsConfigDB["PARSER"]


g_settingsConfig = _SettingsConfig()
