from database.tables import DatabaseTables

from network.commands import COMMAND, Commands as SharedCommands


class Constants:
    SERVER_COMMAND_INIT_DATABASE = "init_db"
    SERVER_COMMAND_INIT_BOOKS = "init"
    TABLE_FOR_AUTHORZATION = DatabaseTables.USERS
    TABLE_ROLES = DatabaseTables.ROLES
    USER_NOT_FOUND_MSG = """Проверьте свои данные."""
    AUTHORIZATION_COMMAND_FAILED_MSG = "Команда не была выполнена."
    CLIENT_IS_NOT_AUTHORIZED_MSG = "Неавторизован."
    ACCESS_ERROR_MSG = "Ощибка доступа."
    CLIENT_NOT_ACCEPTED_MDG = "Клиент не принят."
    COMMAND_NOT_FOUND_MSG = "Команда <{}> не найдена!"
    CREATION_DATE_FIELD = "CreationDate"
    SERVER_INIT_BOOKS_HELP_MSG = """Загрузка данных в справочники."""
    SERVER_INIT_DATABASE_HELP_MSG = """Инициализация базы данных."""


class Commands(SharedCommands):
    SERVER_COMMAND_INIT_DATABASE = COMMAND(-1, Constants.SERVER_COMMAND_INIT_DATABASE, None)
    SERVER_COMMAND_INIT_BOOKS = COMMAND(-2, Constants.SERVER_COMMAND_INIT_BOOKS, None)
    COMMAND_AUTHORIZATION = SharedCommands.COMMAND_AUTHORIZATION
    COMMAND_LOAD_USERS = SharedCommands.COMMAND_LOAD_USERS
    COMMAND_SEARCH_USERS = SharedCommands.COMMAND_SEARCH_USERS
    COMMAND_ADD_USER = SharedCommands.COMMAND_ADD_USER
    COMMAND_DELETE_USER = SharedCommands.COMMAND_DELETE_USER
    COMMAND_UPDATE_USER = SharedCommands.COMMAND_UPDATE_USER
