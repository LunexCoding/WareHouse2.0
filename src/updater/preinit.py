from common import logger
from Logger.log import Logger


logger.logger = Logger()
logger.logger.clearLogs()
logger.logger.setLogSettings("updater", filename="updater.md")
logger.logger.setLogSettings("ftp", filename="ftp.md")
logger.logger.setLogSettings("files", ilename="files.md")
