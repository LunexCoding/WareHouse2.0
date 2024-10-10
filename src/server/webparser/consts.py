from collections import namedtuple

from selenium import webdriver
from selenium.webdriver.common.by import By

DRIVER_FIREFOX_BINARY_PATH = "geckodriver.exe"
TIMEOUT = 3

OPTIONS = ["--headless"]
DRAIVER_OPTIONS = webdriver.FirefoxOptions()
for option in OPTIONS:
    DRAIVER_OPTIONS.add_argument(option)


SELECTOR_TYPE = namedtuple("SelectorType", ["id", "name"])


class SelectorTypes:
    XPATH = By.XPATH
    CLASS = By.CLASS_NAME
    TAG = By.TAG_NAME


SELECTOR = namedtuple("Selector", ["name", "type", "selector"])


class Selectors:
    BODY = SELECTOR("BODY", SelectorTypes.TAG, "body")
    TABLE = SELECTOR("TABLE", SelectorTypes.XPATH, "/html[1]/body[1]/div[1]/div[2]/div[1]/table[1]")
    METAL_INFO_ROWS = SELECTOR("METAL_INFO_ROWS", SelectorTypes.CLASS, "cnt")
    ROW_DATA = SELECTOR("ROW_DATA", SelectorTypes.TAG, "td")

class ParserConstants:
    COLUMN_INDEX_NAME = 2
    COLUMN_INDEX_PRICE = 4
    ITEM_NAME = "Наименование"
    ITEM_PRICE = "Цена"
