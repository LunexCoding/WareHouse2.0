from .commands import CommandFactory

from network.status import CommandStatus
from network.notifications import NotificationType

from common.logger import logger


_log = logger.getLogger(__name__, "app")


class NotificationBase:
    def __init__(self, data):
        self._data = data

    def handle(self, app):
        raise False


class AlertNotification(NotificationBase):
    def __init__(self, data):
        super().__init__(data)

    def handle(self, app):
        app._window.showAlert(self._data)


class CommandNotification(NotificationBase):
    def __init__(self, data):
        super().__init__(data)

    def handle(self, app):
        commandID = self._data.pop(0)
        command = CommandFactory.getCommand(commandID)
        args = self._data
        if command:
            _log.info(f"Выполнение команды: {command.COMMAND_NAME} с аргументами: {args}")
            status, results = command.execute(*args)
            if status == CommandStatus.EXECUTED:
                _log.debug(f"Команда <{command.COMMAND_NAME}> выполнена")
            else:
                _log.debug(f"Команда <{command.COMMAND_NAME}> провалена")
        else:
            _log.error(f"Неизвестная команда: {self._commandID}")


class InfoNotification(NotificationBase):
    def __init__(self, data):
        super().__init__(data)

    def handle(self, app):
        app._window.showInfo(self._data)


class ErrorNotification(NotificationBase):
    def __init__(self, data):
        super().__init__(data)

    def handle(self, app):
        app._window.showError(self._data)


class NotificationFactory:
    _CLASSES = {
        NotificationType.ALERT: AlertNotification,
        NotificationType.COMMAND: CommandNotification,
        NotificationType.INFO: InfoNotification,
        NotificationType.ERROR: ErrorNotification,
    }

    @classmethod
    def getNotificationClass(cls, notificationType):
        try:
            type = NotificationType(int(notificationType))
        except ValueError:
            return None

        return cls._CLASSES.get(type)