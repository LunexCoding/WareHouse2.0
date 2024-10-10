from enum import Enum


class NotificationType(Enum):
    ALERT = 1
    COMMAND = 2
    INFO = 3
    ERROR = 4


class CommandType(Enum):
    UPDATE_FILE = 1
