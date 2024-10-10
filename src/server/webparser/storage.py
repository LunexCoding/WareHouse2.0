import json

from common.config import g_baseConfig
from common.fileSystem import FileSystem


class _Storage:
    def __init__(self):
        self._data = None

    def init(self, data):
        self._data = data

    def readData(self):
        if not FileSystem.exists(g_baseConfig.Data["pricesFile"]):
            return None

        with open(g_baseConfig.Data["pricesFile"], "r", encoding="utf-8") as file:
            self._data = json.load(file)
        return self.data

    def writeData(self):
        with open(g_baseConfig.Data["pricesFile"], "w", encoding="utf-8") as outfile:
            json.dump(self._data, outfile, ensure_ascii=False, indent=4)

    @property
    def data(self):
        return self._data


g_storage = _Storage()
