from common import logger
from Logger.log import Logger


logger.logger = Logger(
    scheduleBackup=True,
    intervalType="minutes",
    intervalValue=1
)
logger.logger.clearLogs()
logger.logger.setLogSettings("server", filename="server.md")
logger.logger.setLogSettings("ftp", filename="ftp.md")
logger.logger.setLogSettings("files", filename="files.md")
logger.logger.setLogSettings("parser", filename="parser.md")
