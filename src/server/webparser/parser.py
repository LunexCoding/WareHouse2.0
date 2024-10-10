from .driver import Browser
from .consts import Selectors, ParserConstants
from .convert import convertStringToNumber

from config import g_settingsConfig


class _Parser:
    def __init__(self, url):
        self._url = url
        self._browser = Browser()

    def extractMetalData(self):
        self._browser.reopen()

        metalData = []

        if not self._browser.openUrl(self._url):
            return None

        table = self._browser.findElement(Selectors.TABLE)
        if table is None:
            return None
            
        rows = self._browser.findElement(Selectors.METAL_INFO_ROWS, element=table, all=True)
        if rows is None:
            return None

        for row in rows:
            columns = self._browser.findElement(Selectors.ROW_DATA, row, all=True)
            if columns is None:
                return None
            
            try:
                name = columns[ParserConstants.COLUMN_INDEX_NAME].text.replace('"', "'")
                price = convertStringToNumber(columns[ParserConstants.COLUMN_INDEX_PRICE].text)
                if price is not None:
                    metalData.append(
                        {
                            "name": name,
                            "price": price
                        }
                    )
            except IndexError:
                continue
            
        self._closeBrowser()
                
        return metalData

    def _closeBrowser(self):
        self._browser.close()


g_parser = _Parser(g_settingsConfig.ParserSettings["url"])
