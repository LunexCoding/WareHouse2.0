import sqlite3
import threading

from config import g_settingsConfig


class DatabaseConnection:
    def __init__(self, databasePath):
        self.__databasePath = databasePath
        self.__local = threading.local()

    def _getConnection(self):
        if not hasattr(self.__local, 'dbConn'):
            self.__local.dbConn = sqlite3.connect(self.__databasePath)
        return self.__local.dbConn

    def execute(self, sql, data=None):
        conn = self._getConnection()
        cursor = conn.cursor()
        if data is not None:
            cursor.execute(sql, data)
        else:
            cursor.execute(sql)
        conn.commit()

    def getData(self, sql, data=None, all=False):
        conn = self._getConnection()
        cursor = conn.cursor()
        if data is not None:
            cursor.execute(sql, data)
        else:
            cursor.execute(sql)
        if all:
            return cursor.fetchall()
        return cursor.fetchone()

    def close(self):
        conn = self._getConnection()
        conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_val, trace):
        try:
            pass
        except AttributeError:
            pass

    def __del__(self):
        self.close()


class DatabaseConnectionFactory:
    def __init__(self, databasePath):
        self.__databasePath = databasePath

    def createConnection(self):
        return DatabaseConnection(self.__databasePath)


databaseSession = DatabaseConnectionFactory(g_settingsConfig.DatabaseSettings["fullPath"])
