from common.logger import createLog

createLog()

from app import App


if __name__ == "__main__":
    app = App()
    app.run()
