import sys
from pathlib import Path

currentDir = Path(__file__).resolve().parent
networkPath = currentDir.parent / "network"
if not networkPath.exists():
    networkPath = currentDir.parent.parent / "network"
sys.path.append(str(networkPath))

currentDir = Path(__file__).resolve().parent
sharedPath = currentDir.parent / "shared"
if not sharedPath.exists():
    sharedPath = currentDir.parent.parent / "shared"
sys.path.append(str(sharedPath))

currentDir = Path(__file__).resolve().parent
commonPath = currentDir.parent / "common"
if not commonPath.exists():
    commonPath = currentDir.parent.parent / "common"
sys.path.append(str(commonPath))

from shared.config import g_settingsConfig

from common.logger import logger


def createLog():
    path = Path(g_settingsConfig.LogSettings["directory"]) / g_settingsConfig.LogSettings["file"]
    if path.exists():
        path.unlink()
    logger.createLog(g_settingsConfig.LogSettings["directory"], g_settingsConfig.LogSettings["file"])
