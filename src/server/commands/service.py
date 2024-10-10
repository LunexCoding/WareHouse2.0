from .command import BaseCommand
import commands.consts as consts

from dataStructures.referenceBook import g_referenceBooks

from initializer.initializer import Initializer

from webparser.parser import g_parser
from webparser.storage import g_storage

from network.notifications import NotificationType, CommandType
from network.status import CommandStatus

from common.ftp import g_ftp
from common.config import g_baseConfig
from common.fileSystem import FileSystem
from common.logger import logger


_log = logger.getLogger(__name__, logName="server")


class ServiceCommand(BaseCommand):
    def __init__(self):
        super().__init__()

    def execute(self, **kwargs):
        baseArgs = []
        kwargs["baseArgs"] = baseArgs
        return self._validateArgs(**kwargs)


class InitDatabase(ServiceCommand):
    COMMAND_NAME = consts.SERVER_COMMAND_INIT_DATABASE

    def __init__(self):
        super().__init__()
        self.msgHelp = consts.SERVER_INIT_DATABASE_HELP_MSG

    def execute(self, **kwargs):
        specificArgs = []
        kwargs["specificArgs"] = specificArgs
        status, missingArgs = super().execute(**kwargs)

        if not status:
            _log.error(consts.NOT_FOUND_ARGS.format(self.COMMAND_NAME, missingArgs))
            return CommandStatus.FAILED, False
        try:
            Initializer.run()
            return CommandStatus.FAILED, False
        except Exception as e:
            _log.debug(e, exc_info=True)
            return CommandStatus.EXECUTED, True



class InitBooks(ServiceCommand):
    COMMAND_NAME = consts.SERVER_COMMAND_INIT_BOOKS

    def __init__(self):
        super().__init__()
        self.msgHelp = consts.SERVER_INIT_BOOKS_HELP_MSG

    def execute(self, **kwargs):
        specificArgs = []
        kwargs["specificArgs"] = specificArgs
        status, missingArgs = super().execute(**kwargs)

        if not status:
            _log.error(consts.NOT_FOUND_ARGS.format(self.COMMAND_NAME, missingArgs))
            return CommandStatus.FAILED, False

        try:
            for book in g_referenceBooks:
                book.init()
            return CommandStatus.EXECUTED, True
        except Exception as e:
            _log.debug(e, exc_info=True)
            return CommandStatus.FAILED, False


class WebParser(ServiceCommand):
    COMMAND_NAME = consts.SERVER_COMMAND_WEBPARSER

    def __init__(self):
        super().__init__()
        self.msgHelp = consts.SERVER_WEBPARSER_HELP_MSG

    def execute(self, **kwargs):
        NOTIFICATION_COMMAND = CommandType.UPDATE_FILE.value
        specificArgs = ["socket"]
        kwargs["specificArgs"] = specificArgs
        status, missingArgs = super().execute(**kwargs)

        if not status:
            _log.error(consts.NOT_FOUND_ARGS.format(self.COMMAND_NAME, missingArgs))
            return CommandStatus.FAILED, False

        socket = kwargs.get("socket")

        try:
            _log.debug("Запуск парсера...")
            data = g_parser.extractMetalData()
            if data is None:
                return CommandStatus.FAILED, False
            
            if not data:
                return CommandStatus.FAILED, False
            
            g_storage.init(data)
            g_storage.writeData()

            if not FileSystem.exists(g_baseConfig.Data["pricesFile"]):
                return CommandStatus.FAILED, False
            
            if not g_ftp.uploadFile(g_baseConfig.Data["pricesFile"], g_baseConfig.Data["pricesFile"]):
                return CommandStatus.FAILED, False
            
            _log.debug("Отпрвка уведомления парсера...")
            notificationType = NotificationType.COMMAND.value
            args = [
                str(NOTIFICATION_COMMAND),
                g_baseConfig.Data["pricesFile"],
                g_baseConfig.Data["pricesFile"]
            ]
            socket.sendNotifications(notificationType, args)

            return CommandStatus.EXECUTED, True
            
        except Exception as e:
            _log.error(e, exc_info=True)
            return CommandStatus.FAILED, False


COMMANDS = {
    InitDatabase.COMMAND_NAME: InitDatabase,
    InitBooks.COMMAND_NAME: InitBooks,
    WebParser.COMMAND_NAME: WebParser
}
