from customtkinter import CTkButton, CTkFrame, E

from user import g_user

from .markup import MARCUP, TypesUiMarkups
from .widget import BaseWidget
import ui.contexts.consts as contextConstants

from commands.roles import Roles, RolesInt



class CommandButtonsWidget(BaseWidget):
    def __init__(self, master, commands):
        super().__init__(master)
        self.buttonFrame = CTkFrame(master)
        self.buttonCreate = CTkButton(self.buttonFrame, text=contextConstants.BUTTON_CREATE, font=contextConstants.FONT, command=commands["create"])
        self.buttonSearch = CTkButton(self.buttonFrame, text=contextConstants.BUTTON_SEARCH, font=contextConstants.FONT, command=commands["search"])
        self.buttonRemove = CTkButton(self.buttonFrame, text=contextConstants.BUTTON_DELETE, font=contextConstants.FONT, command=commands["remove"])
        self._uiElements.append(MARCUP(element=self.buttonFrame, type=TypesUiMarkups.GRID, row=0, column=2, padx=10, pady=10))
        self._uiElements.append(MARCUP(element=self.buttonSearch, type=TypesUiMarkups.GRID, row=0, column=3, padx=10, pady=10))
        self._uiElements.append(MARCUP(element=self.buttonCreate, type=TypesUiMarkups.GRID, row=0, column=4, padx=10, pady=10))
        if g_user.role in [Roles.getRole(RolesInt.ADMIN)]:
            self._uiElements.append(MARCUP(element=self.buttonRemove, type=TypesUiMarkups.GRID, row=0, column=5, pady=10, padx=10))

        self.exitFrame = CTkFrame(master)
        self.buttonBack = CTkButton(self.exitFrame, text=contextConstants.BUTTON_BACK, font=contextConstants.FONT, command=commands["back"])
        self._uiElements.append(MARCUP(element=self.exitFrame, type=TypesUiMarkups.GRID, row=0, column=6, padx=10, pady=10, sticky=E))
        self._uiElements.append(MARCUP(element=self.buttonBack, type=TypesUiMarkups.PACK, padx=10, pady=10))
        self.show()
