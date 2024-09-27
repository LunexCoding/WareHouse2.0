from customtkinter import CTkFrame, CTkLabel

from .markup import MARCUP, TypesUiMarkups
from .widget import BaseWidget
from ui.contexts.consts import Constants

from user import g_user


class UserInfoWidget(BaseWidget):
    def __init__(self, master):
        super().__init__(master)
        self.userFrame = CTkFrame(master)
        self.userRoleLabel = CTkLabel(self.userFrame, text=g_user.role, font=Constants.FONT)
        self.userFullnameLabel = CTkLabel(self.userFrame, text=g_user.fullname, font=Constants.FONT)
        self._uiElements.append(MARCUP(element=self.userFrame, type=TypesUiMarkups.GRID, padx=10, pady=10))
        self._uiElements.append(MARCUP(element=self.userRoleLabel, type=TypesUiMarkups.PACK, padx=10, pady=10))
        self._uiElements.append(MARCUP(element=self.userFullnameLabel, type=TypesUiMarkups.PACK, row=0, column=0, padx=10, pady=10))
        self.show()
