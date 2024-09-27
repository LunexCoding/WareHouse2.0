import os
import sys


class Constants:
    LOCAL_DOWNLOAD_PATH = "_internal"
    LOCAL_VERSION_FILE = "version.txt"
    FILE_PREFIX = "client_"
    FILE_EXTENSION = "zip"
    CLIENT_EXE = "client.exe"
    UPDATER_PATH = os.path.dirname(os.path.abspath(sys.executable))
    CLIENT_PATH = os.path.abspath(os.path.join(UPDATER_PATH, os.pardir, CLIENT_EXE))
    FILES_FOR_DELETION = [
        CLIENT_PATH
    ]
   