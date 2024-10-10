from .queries import SqlQueries

from config import g_settingsConfig

from database.pipeline import DatabasePipeline
from database.queries import SqlQueries as coreQueries
from database.tables import DatabaseTables

from common.fileSystem import FileSystem
from common.logger import logger


_log = logger.getLogger(__name__, logName="server")


class Initializer:
    @staticmethod
    def initializeDatabase():
        _log.debug("Database creation...")
        databaseCreationPipeline = DatabasePipeline()
        databaseCreationPipeline.addOperation(SqlQueries.applyingSettings)
        databaseCreationPipeline.addOperation(SqlQueries.createTableRoles)
        databaseCreationPipeline.addOperation(SqlQueries.createTableUsers)
        databaseCreationPipeline.run()

    @staticmethod
    def initializeDatabaseTriggers():
        _log.debug("Creating triggers...")

    @staticmethod
    def initializeDatabaseData():
        _log.debug("Data recording...")
        record = DatabasePipeline()
        record.addOperation(coreQueries.insertIntoTable(DatabaseTables.ROLES, ["Name"]), ["Admin"])
        record.addOperation(coreQueries.insertIntoTable(DatabaseTables.ROLES, ["Name"]), ["User"])
        record.addOperation(coreQueries.insertIntoTable(DatabaseTables.USERS, ["Login", "Password", "RoleID"]), ["admin", "admin", 1])
        record.addOperation(coreQueries.insertIntoTable(DatabaseTables.USERS, ["Login", "Password", "RoleID"]), ["user", "user", 2])
        record.run()

    @staticmethod
    def run():
        if not FileSystem.exists(g_settingsConfig.DatabaseSettings["databaseDirectory"]):
            _log.debug("Creating a directory for the database...")
            FileSystem.makeDir(g_settingsConfig.DatabaseSettings["databaseDirectory"])
        if not FileSystem.exists(g_settingsConfig.DatabaseSettings["fullPath"]):
            _log.debug("Initializing the Database...")
            Initializer.initializeDatabase()
            Initializer.initializeDatabaseTriggers()
            Initializer.initializeDatabaseData()
            _log.debug("Database initialized.")
            return True
        else:
            _log.debug("The database already exists.")
            return False
