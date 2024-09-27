from commands.command import BaseCommand
from dataStructures.referenceBook import g_referenceBooks
from initializer.initializer import Initializer
from commands.consts import Constants

from common.logger import logger


_log = logger.getLogger(__name__)


class ServiceCommand(BaseCommand):
    def __init__(self):
        super().__init__()


class InitDatabase(ServiceCommand):
    COMMAND_NAME = Constants.SERVER_COMMAND_INIT_DATABASE

    def __init__(self):
        super().__init__()
        self.msgHelp = Constants.SERVER_INIT_DATABASE_HELP_MSG

    def execute(self, client=None, commandArgs=None):
        return Initializer.run()


class InitBooks(ServiceCommand):
    COMMAND_NAME = Constants.SERVER_COMMAND_INIT_BOOKS

    def __init__(self):
        super().__init__()
        self.msgHelp = Constants.SERVER_INIT_BOOKS_HELP_MSG

    def execute(self, client=None, commandArgs=None):
        try:
            for book in g_referenceBooks:
                book.init()
            return True
        except Exception as e:
            _log.debug(e)
            return False


COMMANDS = {
    InitDatabase.COMMAND_NAME: InitDatabase,
    InitBooks.COMMAND_NAME: InitBooks
}
