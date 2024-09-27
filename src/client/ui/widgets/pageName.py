from customtkinter import CTkFrame, CTkLabel

from .markup import MARCUP, TypesUiMarkups
from .widget import BaseWidget
from ui.contexts.consts import Constants


class PageNameWidget(BaseWidget):
    def __init__(self, master, pageName):
        super().__init__(master)
        self.pageNameFrame = CTkFrame(master)
        self.pageNameLabel = CTkLabel(self.pageNameFrame, text=pageName, font=Constants.FONT)
        self.pageNameLabel.pack(padx=10, pady=10)
        self.pageNameFrame.grid(row=0, column=1, padx=10, pady=10)
        self._uiElements.append(MARCUP(element=self.pageNameFrame, type=TypesUiMarkups.GRID, row=0, column=1, padx=10, pady=10))
        self._uiElements.append(MARCUP(element=self.pageNameLabel, type=TypesUiMarkups.PACK, padx=10, pady=10))
        self.show()
