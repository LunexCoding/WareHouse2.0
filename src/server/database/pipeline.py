from collections import namedtuple

from .database import databaseSession


OPERATION = namedtuple("Operation", ["query", "data"])


class DatabasePipeline:
    def __init__(self):
        self.__operations = []

    def addOperation(self, operation, data=None):
        self.__operations.append(OPERATION(query=operation, data=data))

    def run(self):
        with databaseSession.createConnection() as db:
            for operation in self.__operations:
                if operation.data is not None:
                    db.execute(operation.query, operation.data)
                else:
                    db.execute(operation.query)
        self.__clear()

    def __clear(self):
        self.__operations.clear()
