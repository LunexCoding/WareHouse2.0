from common.logger import createLog

createLog()

from updater import Updater


if __name__ == "__main__":
    updater = Updater()
    updater.run()
