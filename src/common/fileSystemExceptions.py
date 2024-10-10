class BasePathException(OSError):
    def __init__(self, path, message):
        self._path = path
        self._message = message


class PathExistsException(BasePathException):
    def __str__(self):
        return f"Путь существует: {self._path}"


class PathExistsAsFileException(BasePathException):
    def __str__(self):
        return f"Путь существует как файл, не как директория: {self._path}"
    

class FileDeletionException(BasePathException):
    def __str__(self):
        if self._message:
            return f"Ошибка при удалении: {self._path} по причине {self._message}"
        return f"Ошибка при удалении: {self._path}"


class FileExtractionException(BasePathException):
    def __str__(self):
        if self._message:
            return f"Ошибка при распаковке архива: {self._path} по причине {self._message}"
        return f"Ошибка при распаковке архива: {self._path}"


class FileNotFoundException(BasePathException):
    def __str__(self):
        return f"Файл не найден: {self._path}"


class FileCopyException(BasePathException):
    def __str__(self):
        if self._message:
            return f"Ошибка копирования файла: {self._path} по причине {self._message}"
        return f"Ошибка копирования файла: {self._path}"
