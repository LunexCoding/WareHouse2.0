from commands.roles import ROLES_FOR_INPUT

from dataStructures.dataObjs.dataObj import DataObj

import ui.contexts.popup.consts as contextsConstants
from ui.widgets.consts import WidgetConstants


class User(DataObj):
    _FIELDS = {
        "ID": {
            "text": "Номер",
            "size": contextsConstants.ENTRY_WIDTH
        },
        "Login": {
            "text": "Логин",
            "size": contextsConstants.ENTRY_WIDTH,
            "type": str,
            "widget": WidgetConstants.ENTRY
        },
        "Password": {
            "text": "Пароль",
            "size": contextsConstants.ENTRY_WIDTH,
            "type": str,
            "widget": WidgetConstants.ENTRY
        },
        "RoleID": {
            "text": "Роль",
            "size": contextsConstants.ENTRY_WIDTH,
            "type": int,
            "widget": WidgetConstants.COMBOBOX,
            "options": ROLES_FOR_INPUT
        },
        "Fullname": {
            "text": "ФИО",
            "size": contextsConstants.ENTRY_WIDTH,
            "type": str,
            "widget": WidgetConstants.ENTRY
        }
    }
    _INPUT_FIELDS = ["Login", "Password", "RoleID", "Fullname"]
    _EDIT_FIELDS = ["Login", "Password", "RoleID", "Fullname"]
    _MAIN_INPUT_FIELDS = ["Client"]

    def __init__(self, id, login, password, roleID, fullname):
        self._id = int(id)
        self._login = login
        self._password = password
        self._roleID = roleID
        self._fullname = fullname

    @property
    def data(self):
        return {
            "ID": self._id,
            "Login": self._login,
            "Password": self._password,
            "RoleID": self._roleID,
            "Fullname": self._fullname
        }
