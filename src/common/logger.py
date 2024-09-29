from pathlib import Path

from Logger import Logger

logger = Logger()


def createLog(dir="./logs", filename="log.md"):
    path = Path(dir) / filename
    if path.exists():
        path.unlink() 
    logger.createLog(dir, filename)
