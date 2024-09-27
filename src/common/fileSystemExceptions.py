class BasePathException(OSError):
    def __init__(self, path):
        self._path = path


class PathExistsException(BasePathException):
    def __str__(self):
        return f"Path <{self._path}> exists"


class PathExistsAsFileException(BasePathException):
    def __str__(self):
        return f"Path <{self._path}> exists as a file, not as a directory"
    

class FileDeletionException(BasePathException):
    def __init__(self, path, message):
        super().__init__(path)
        self.message = message

    def __str__(self):
        return f"Failed to delete <{self._path}>: {self.message}"


class FileExtractionException(BasePathException):
    def __init__(self, path):
        self.path = path
        super().__init__(f"Ошибка при распаковке архива: {self.path}")


class FileNotFoundException(BasePathException):
    def __init__(self, path):
        self.path = path
        super().__init__(f"Файл не найден: {self.path}")


class FileCopyException(BasePathException):
    
    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"Ошибка копирования файла: {self.message}"
