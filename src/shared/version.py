from packaging.version import Version

from common.fileSystem import FileSystem


class VersionChecker:
    @classmethod
    def checkVersion(cls, localVersionFilePath, prefix, extension, ftp):
        localVersion = cls._getLocalVersion(localVersionFilePath)
        file, remoteVersion = ftp.findVersionedFile(prefix, extension)
        if file and remoteVersion is not None:
            if remoteVersion > localVersion:
                return file, remoteVersion
            return None, None
        return None, None
            
    @staticmethod
    def _getLocalVersion(versionFilePath):
        if FileSystem.exists(versionFilePath):
            with open(versionFilePath, "r") as file:
                return Version(file.read().strip())
        return Version("0.0.0")
    