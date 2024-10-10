import shutil
import zipfile
from pathlib import Path
from datetime import datetime

from .fileSystemExceptions import (
    PathExistsException,
    PathExistsAsFileException,
    FileDeletionException,
    FileExtractionException,
    FileNotFoundException,
    FileCopyException
)
from .logger import logger


_log = logger.getLogger(__name__, "files")


class FileSystem:
    @staticmethod
    def exists(path):
        return Path(path).exists()

    @staticmethod
    def makeDir(path, recreate=False):
        path = Path(path)

        if path.exists() and path.is_file():
            raise PathExistsAsFileException(path)
        
        if path.exists() and recreate is False:
            _log.error(f"Директория уже существует: {path}")
            raise PathExistsException(path)
        
        if path.exists() and recreate:
            _log.debug(f"Директория уже существует: {path}")

        if not path.exists():
            _log.debug(f"Директория создана: {path}")

        path.mkdir(parents=True, exist_ok=recreate)
        return True
    
    @staticmethod
    def unzip(zipFilePath, extractToPath):
        zipFilePath = Path(zipFilePath)
        extractToPath = Path(extractToPath)

        if not zipFilePath.is_file():
            _log.error(f"Архив не найден: {zipFilePath}")
            raise FileNotFoundException(zipFilePath)

        if not extractToPath.exists():
            try:
                FileSystem.makeDir(extractToPath)
            except Exception as e:
                _log.error(f"Ошибка при создании директории <{extractToPath}>: {e}")
                raise FileExtractionException(extractToPath, e)

        try:
            with zipfile.ZipFile(zipFilePath, 'r') as zip_ref:
                zip_ref.extractall(extractToPath)
            _log.info(f"Архив <{zipFilePath}> успешно распакован в <{extractToPath}>")

        except Exception as e:
            _log.error(f"Ошибка при распаковке архива <{zipFilePath}>: {e}")
            raise FileExtractionException(zipFilePath, e)

        return True

    @staticmethod
    def deleteFile(path):
        filePath = Path(filePath)

        if not filePath.exists():
            _log.debug(f"Файл не существует: {filePath}")
            return True

        if not filePath.is_file():
            _log.error(f"Файл не найден: {filePath}")
            raise FileNotFoundException(filePath)

        try:
            filePath.unlink()
            _log.info(f"Файл {filePath} успешно удален")
        except Exception as e:
            _log.error(f"Ошибка при удалении файла {filePath}: {e}")
            raise FileDeletionException(filePath, e)

        return True

    @staticmethod
    def copyFile(src, dest, overwrite=False):
        src = Path(src)
        dest = Path(dest)

        if not src.is_file():
            _log.error(f"Исходный файл не найден: {src}")
            raise FileNotFoundException(src)

        if dest.exists() and not overwrite:
            _log.error(f"Файл {dest} уже существует.")
            raise PathExistsException(dest)

        try:
            shutil.copy2(src, dest)
            _log.info(f"Файл {src} успешно скопирован в {dest}")
        except Exception as e:
            _log.error(f"Ошибка при копировании файла {src} в {dest}: {e}")
            raise FileCopyException(message=e)

        return True
    
    @staticmethod
    def joinPaths(*paths):
        return Path(*paths)

    @staticmethod
    def createUniqueFile(path):
        filePath = Path(path)
        if not filePath.exists():
            filePath.touch()
            return filePath

        baseName = filePath.stem
        ext = filePath.suffix
        index = 1
        while True:
            newFilePath = filePath.with_name(f"{baseName} ({index}){ext}")
            if not newFilePath.exists():
                newFilePath.touch()
                return newFilePath
            index += 1

    @staticmethod
    def joinPaths(*paths):
        return Path(*paths)

    @staticmethod
    def moveFile(src, dest):
        shutil.move(str(src), str(dest))

    @staticmethod
    def getModificationTime(path):
        filePath = Path(path)
        
        if not filePath.exists():
            return None

        modifiedTime = filePath.stat().st_mtime
        dt = datetime.fromtimestamp(modifiedTime)
        return dt

    @staticmethod
    def compareTimestamps(first, second):
        if first is None:
            return False
        
        if second is None:
            return True

        if first > second:
            return True
        return False
