from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.common.exceptions import NoSuchElementException, TimeoutException, JavascriptException

from . import consts

from config import g_settingsConfig

from common.fileSystem import FileSystem
from common.logger import logger


_log = logger.getLogger(__name__, logName="parser")


class Browser:
    def __init__(self):
        self._driver = self._setupDriver()

    def _setupDriver(self):
        customPath = g_settingsConfig.DataSettings["driversDir"]
        if not FileSystem.exists(customPath):
            FileSystem.makeDir(customPath)

        driverPath = FileSystem.joinPaths(customPath, consts.DRIVER_FIREFOX_BINARY_PATH)
        _log.debug(f"Driver path: {driverPath}")

        if not FileSystem.exists(driverPath):
            _log.info("geckodriver не найден. Скачивание...")
            downloadedDriverPath = GeckoDriverManager().install()
            FileSystem.moveFile(downloadedDriverPath, driverPath)
            _log.info("geckodriver успешно скачан и перемещен в: %s", driverPath)
        else:
            _log.info("geckodriver найден по пути: %s", driverPath)

        driver = webdriver.Firefox(service=FirefoxService(driverPath), options=consts.DRAIVER_OPTIONS)

        driver.set_page_load_timeout(consts.TIMEOUT)
        return driver

    def openUrl(self, url, stop_on_timeout=True):
        try:
            prevUrl = self._driver.current_url
            self._driver.get(url)

            _log.debug(f"Open url: {url}")
            _log.debug(f"{prevUrl} -> {self._driver.current_url}")
            return True
        
        except TimeoutException:
            if stop_on_timeout:
                self._stopLoadingPage()

            try:
                element = self.findElement(consts.Selectors.BODY)
                if element is not None:
                    _log.debug("Страница загрузилась, но с таймаутом.")
                    return True

            except TimeoutException:
                _log.error("Страница не загрузилась.")
                return False

        except Exception as e:
            _log.error(f"Произошла ошибка при открытии страницы", exc_info=True)
            return False

    def findElement(self, selector, element=None, all=False, retry=False):
        selectorName = selector.name
        typeSelector = selector.type
        selector = selector.selector
        _log.debug(f"Searching element {selectorName} by {str(typeSelector)}...")
        if retry:
            return self._findElementWithRetry(selector, typeSelector, element, all)
        return self._findElement(selector, typeSelector, element, all)

    def reopen(self):
        if self._driver is None:
            _log.debug("Повторное открытие браузера...")
            self._driver = self._setupDriver()
        else:
            _log.debug("Браузер уже открыт.")

    def close(self):
        self._driver.quit()
        self._driver = None
        _log.debug("Закрытие браузера")

    def _stopLoadingPage(self):
        self._driver.execute_script("window.stop();")
        _log.debug(f"Загрузка страницы <{self._driver.current_url}> была остановлена")

    def _findElementWithRetry(self, selector, typeSelector, element, all):
        attempt = 0
        while attempt < 2:
            attempt += 1
            try:
                return self._findElement(selector, typeSelector, element, all)
            except (TimeoutException, NoSuchElementException, JavascriptException):
                _log.debug("Повторная попытка...")
                continue
        _log.debug("Достигнуто максимальное количество попыток. Элемент не найден.")
        return None

    def _findElement(self, selector, typeSelector, element, all):
        if element is None:
            if all:
                elements = self._driver.find_elements(typeSelector, selector)
                if not elements:
                    return None
                return elements
            return self._driver.find_element(typeSelector, selector)
        else:
            if all:
                elements = element.find_elements(typeSelector, selector)
                if not elements:
                    return None
                return elements
            return element.find_element(typeSelector, selector)
