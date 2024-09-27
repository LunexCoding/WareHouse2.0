import shutil
import zipfile
from pathlib import Path

from .fileSystemExceptions import (
    PathExistsException,
    PathExistsAsFileException,
    FileDeletionException,
    FileExtractionException,
    FileNotFoundException,
    FileCopyException
)

from .logger import logger

_log = logger.getLogger(__name__)


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
            raise PathExistsException(path)
        
        path.mkdir(exist_ok=recreate)
        return True

    @staticmethod
    def deleteFile(filePath):
        try:
            file = Path(filePath)
            if file.is_file():
                file.unlink()
                _log.info(f"Файл {filePath} успешно удалён.")
            else:
                _log.error(f"{filePath} не является файлом.")
        except Exception as e:
            _log.error(f"Ошибка при удалении файла {filePath}: {e}")
            raise FileDeletionException(filePath) from e
    
    @staticmethod
    def unzip(zipFilePath, extractTo):
        zipFilePath = Path(zipFilePath)
        extractTo = Path(extractTo)

        if not zipFilePath.is_file():
            _log.error(f"Архив не найден: {zipFilePath}")
            raise FileNotFoundException(f"Архив не найден: {zipFilePath}")

        if not extractTo.exists():
            try:
                FileSystem.makeDir(extractTo)
            except Exception as e:
                _log.error(f"Ошибка при создании директории {extractTo}: {e}")
                raise FileExtractionException(f"Ошибка при создании директории {extractTo}") from e

        try:
            with zipfile.ZipFile(zipFilePath, 'r') as zip_ref:
                zip_ref.extractall(extractTo)
            _log.info(f"Архив {zipFilePath} успешно распакован в {extractTo}")

        except Exception as e:
            _log.error(f"Ошибка при распаковке архива {zipFilePath}: {e}")
            raise FileExtractionException(f"Ошибка при распаковке архива {zipFilePath}") from e

        return True

    @staticmethod
    def deleteFile(filePath):
        filePath = Path(filePath)

        if not filePath.is_file():
            _log.error(f"Файл не найден: {filePath}")
            raise FileNotFoundException(f"Файл не найден: {filePath}")

        try:
            filePath.unlink()
            _log.info(f"Файл {filePath} успешно удален")
        except Exception as e:
            _log.error(f"Ошибка при удалении файла {filePath}: {e}")
            raise FileDeletionException(f"Ошибка при удалении файла {filePath}") from e

        return True

    @staticmethod
    def copyFile(src, dest, overwrite=False):
        src = Path(src)
        dest = Path(dest)

        if not src.is_file():
            _log.error(f"Исходный файл не найден: {src}")
            raise FileNotFoundException(f"Исходный файл не найден: {src}")

        if dest.exists() and not overwrite:
            _log.error(f"Файл {dest} уже существует.")
            raise PathExistsException(f"Файл {dest} уже существует.")

        try:
            shutil.copy2(src, dest)
            _log.info(f"Файл {src} успешно скопирован в {dest}")
        except Exception as e:
            _log.error(f"Ошибка при копировании файла {src} в {dest}: {e}")
            raise FileCopyException(f"Ошибка при копировании файла {src} в {dest}") from e

        return True