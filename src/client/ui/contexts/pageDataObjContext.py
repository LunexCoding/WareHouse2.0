from customtkinter import END, CTkButton, CTkFrame, Y

from . import consts
from .context import Context
from ..widgets import CommandButtonsWidget, PageNameWidget, TableWidget, UserInfoWidget
from ..widgets.table import DataObjContext, DataObjContextType


class PageDataObjContext(Context):
    def __init__(self, window, data):
        super().__init__(window, data)

        self._referenceBook = data["book"]
        self._dataObj = self._referenceBook.dataObj
        window.title(self._referenceBook.table)

        self.frame = CTkFrame(window)

        UserInfoWidget(self.frame)
        PageNameWidget(self.frame, self._referenceBook.table)
        CommandButtonsWidget(
            self.frame,
            commands={
                "create": self._onButtonCreateClicked,
                "search": self._onButtonSearchClicked,
                "remove": self._onButtonRemoveClicked,
                "back": self._onButtonBackClicked
            }
        )

        self.frame.pack(fill=Y, padx=10, pady=10)

        self.table = TableWidget(window, self._dataObj, self._editRow)

        self.buttonLoad = CTkButton(window, text=consts.BUTTON_LOAD_MORE, font=consts.FONT, command=self._onButtonLoadClicked)
        self.buttonLoad.pack(padx=20, pady=20)
        self._loadRows()

    def _onButtonCreateClicked(self):
        self._window.openTopLevel(
            DataObjContext,
            {
                "name": consts.POPUP_WINDOW_NAME_INPUT,
                "command": self._saveRow,
                "dataObj": self._dataObj,
                "contextType": DataObjContextType.INPUT
            }
        )

    def _onButtonSearchClicked(self):
        ...

    def _onButtonRemoveClicked(self):
        selectedItem = self.table.selectedItem
        if selectedItem:
            rowID = selectedItem["values"][0]
            if self._referenceBook.removeRow(rowID) is not None:
                self.table.deleteRow(self.table.tree.selection()[0])

    def _onButtonBackClicked(self):
        window = self._window
        self.clear()
        window.returnToPrevious()

    def _onButtonLoadClicked(self):
        rows = self._referenceBook.loadRows()
        if rows is not None:
            self.displayRows(rows)

    def _saveRow(self, row):
        self._window.topLevelWindow.close()
        result = self._referenceBook.addRow(row)
        if result is not None:
            self.displayRows([result])

    def _editRow(self, row):
        self._window.topLevelWindow.close()
        newRow = self._referenceBook.updateRow(row)
        self.table.updateRow(newRow)

    def _loadRows(self):
        if not self._referenceBook.rows:
            while True:
                rows = self._referenceBook.loadRows()
                if rows is None:
                    break
                self.displayRows(rows)
        else:
            self.displayRows(self._referenceBook.rows)

    def displayRows(self, rows):
        if rows is not None:
            for row in rows:
                self.table.insertRow("", END, values=list(row.data.values()))
