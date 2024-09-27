from tkinter.ttk import Scrollbar, Treeview

from customtkinter import BOTH, CENTER, LEFT, RIGHT, TOP, VERTICAL, CTkFrame, Y

from .markup import MARCUP, TypesUiMarkups
from .widget import BaseWidget
from .errorLabel import ErrorLabel
from ui.contexts.consts import Constants
from ui.contexts.popup.dataObjContext import DataObjContext
from ui.contexts.popup.consts import DataObjContextType

from user import g_user

from commands.roles import Roles, RolesInt


class TableWidget(BaseWidget):
    def __init__(self, master, dataObj, editCommand):
        super().__init__(master)
        self._window = master
        self._dataObj = dataObj
        self._editCommand = editCommand
        self._columns = self._dataObj.getFields()
        self._selectedItem = None
        self._count = 1

        self.tableFrame = CTkFrame(self._window)
        self.errorLabel = ErrorLabel(master=self.master, text_color=Constants.ERROR_LABEL_MSG_COLOR, font=Constants.FONT)
        self.tree = Treeview(self.tableFrame, columns=list(self._columns.keys()))
        for header, option in self._columns.items():
            self.tree.heading(header, text=option["text"])
            self.tree.column(header, width=option["size"], anchor=CENTER)
        self.tree.column("#0", width=0, stretch=False)
        self.treeScroll = Scrollbar(self.tableFrame, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.treeScroll.set)
        self._uiElements.append(MARCUP(element=self.tableFrame, type=TypesUiMarkups.PACK, side=TOP, fill=BOTH, expand=True, pady=10, padx=10))
        self._uiElements.append(MARCUP(element=self.treeScroll, type=TypesUiMarkups.PACK, side=RIGHT, fill=Y))
        self._uiElements.append(MARCUP(element=self.tree, type=TypesUiMarkups.PACK, side=LEFT, fill=BOTH, expand=True))
        self.tree.bind("<Double-1>", self._onDoubleClicked)
        self.tree.bind("<<TreeviewSelect>>", self._onSelectClicked)
        self.show()

    def insertRow(self, *args, **kwargs):
        self.tree.insert(iid=str(self._count), *args, **kwargs)
        self._count += 1

    def updateRow(self, dataObj):
        self.tree.item(str(dataObj.data["ID"]), values=list(dataObj.data.values()))

    def deleteRow(self, *items):
        self.tree.delete(*items)
        self._selectedItem = None

    def _onDoubleClicked(self, event):
        item = self.tree.selection()
        if g_user.role in [Roles.getRole(RolesInt.ADMIN)]:
            if item:
                itemObj = self._dataObj(*self.tree.item(item, "values"))
                self._createInfoPopupWindow(itemObj)
        else:
            self.errorLabel.setText("Ошибка доступа")
            self.errorLabel.show()

    def _onSelectClicked(self, event):
        selectedItem = self.tree.selection()
        if selectedItem:
            self._selectedItem = self.tree.item(selectedItem[0])

    def _createInfoPopupWindow(self, item):
        self._window.openTopLevel(
            DataObjContext,
            {
                "name": Constants.POPUP_WINDOW_NAME_INFO,
                "item": item,
                "command": self._editCommand,
                "contextType": DataObjContextType.INFO
            }
        )

    @property
    def selectedItem(self):
        return self._selectedItem
