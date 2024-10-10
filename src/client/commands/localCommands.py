import notifications.consts as consts

from network.status import CommandStatus

from common.fileSystem import FileSystem
from common.ftp import g_ftp
from common.logger import logger


_log = logger.getLogger(__name__, "files")


class LocalCommandBase:
    COMMAND_NAME = None
    
    def execute(self):
        raise False
    

class UpdateFile(LocalCommandBase):
    COMMAND_NAME = consts.COMMAND_UPDATE_FILE

    def execute(self, remotePath, localpath):
        try:
            remoteTime = g_ftp.getModificatioTime(remotePath)
            localTime = FileSystem.getModificationTime(localpath)
            if not FileSystem.compareTimestamps(remoteTime, localTime):
                _log.debug(f"Файл актуален: {localpath}")
                return CommandStatus.EXECUTED, None

            status = g_ftp.downloadFile(remotePath, localpath)
            if not status:
                return CommandStatus.FAILED, None
            return CommandStatus.EXECUTED, None
        
        except Exception as e:
            _log.error(e, exc_info=True)
            return CommandStatus.FAILED, None
