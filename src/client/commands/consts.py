from network.commands import Constants


class Constants:
    DEFAULT_COMMAND_STRING = "{}.{}.{}".replace(".", Constants.SERVICE_SYMBOL)
    COMMAND_UPDATE_STRING = "{}.{}.{}.{}".replace(".", Constants.SERVICE_SYMBOL)
    COMMAND_DELETE_STRING = "{}.{}".replace(".", Constants.SERVICE_SYMBOL)
