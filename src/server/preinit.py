import sys
from pathlib import Path

currentDir = Path(__file__).resolve().parent
networkPath = currentDir.parent / "network"
if not networkPath.exists():
    networkPath = currentDir.parent.parent / "network"
sys.path.append(str(networkPath))

currentDir = Path(__file__).resolve().parent
commonPath = currentDir.parent / "common"
if not commonPath.exists():
    commonPath = currentDir.parent.parent / "common"
sys.path.append(str(commonPath))

from config import g_settingsConfig
from common.logger import logger

def createLog():
    logger.createLog(g_settingsConfig.LogSettings["directory"], g_settingsConfig.LogSettings["file"], True)
