import os


CLIENT_IS_NOT_CONNECTED_MSG = "Клиент не подключен"
SENT_MSG = "Sent\tdata: ID<{}> {}"
RECEIVED_MSG = "Received\tdata: {}"
UPDATER_LOCAL_VERSION_FILE = os.path.join(os.path.dirname(__file__), "updaterVersion.txt")
UPDATER_FILE_PREFIX = "updater_"
UPDATER_FILE_EXTENSION = "exe"
UPDATER = os.path.join(os.path.dirname(__file__), "updater.exe")
CLIENT_VERSION_FILE = os.path.join(os.path.dirname(__file__), "version.txt")
CLIENT_FILE_PREFIX = "client_"
CLIENT_FILE_EXTENSION = "zip"
