import sqlite3
import threading

from config import g_settingsConfig


class DatabaseConnection:
    def __init__(self, databasePath):
        self.__databasePath = databasePath
        self.__lock = threading.Lock()
        self.__dbConn = sqlite3.connect(self.__databasePath)

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_val, trace):
        try:
            pass
        except AttributeError:
            pass

    def execute(self, sql, data=None):
        with self.__lock:
            cursor = self.__dbConn.cursor()
            if data is not None:
                cursor.execute(sql, data)
            else:
                cursor.execute(sql)
            self.__dbConn.commit()

    def getData(self, sql, data=None, all=False):
        with self.__lock:
            cursor = self.__dbConn.cursor()
            if data is not None:
                cursor.execute(sql, data)
            else:
                cursor.execute(sql)
            if all:
                return cursor.fetchall()
            return cursor.fetchone()

    def close(self):
        self.__dbConn.close()

    def __del__(self):
        self.close()


class DatabaseConnectionFactory:
    def __init__(self, databasePath):
        self.__databasePath = databasePath

    def createConnection(self):
        return DatabaseConnection(self.__databasePath)


databaseSession = DatabaseConnectionFactory(g_settingsConfig.DatabaseSettings["fullPath"])
