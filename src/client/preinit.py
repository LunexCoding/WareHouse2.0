from common.logger import logger


logger.clearLogs()
logger.setLogSettings("app", filename="app.md")
logger.setLogSettings("updater", filename="updater.md")
logger.setLogSettings("ftp", filename="ftp.md")
logger.setLogSettings("files", filename="files.md")
logger.setLogSettings("parser", filename="parser.md")
