import sys
from pathlib import Path

from common.fileSystem import FileSystem


LOCAL_DOWNLOAD_PATH = "_internal"
LOCAL_VERSION_FILE = "version.txt"
FILE_PREFIX = "client_"
FILE_EXTENSION = "zip"
CLIENT_EXE = "client.exe"
UPDATER_PATH = Path(sys.executable).parent
CLIENT_PATH = FileSystem.joinPaths(UPDATER_PATH.parent, CLIENT_EXE)
FILES_FOR_DELETION = [
    CLIENT_PATH
]
   