from pathlib import Path

from Logger import Logger

logger = Logger()


def createLog(dir="./logs", filename="log.md"):
    path = Path(dir) / filename
    if path.exists():
        path.unlink() 
    with path.open(mode='w', encoding='utf-8') as file: ...
    logger.createLog(dir, filename)
