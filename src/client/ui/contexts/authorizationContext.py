from customtkinter import CTkButton, CTkEntry, CTkLabel

from . import consts
from .context import Context
from .mainContext import MainWindowContext

from user import g_user


class AuthorizationWindowContext(Context):
    def __init__(self, window, data):
        super().__init__(window, data)
        self.button = CTkButton(master=window, text="Войти", command=self._login)
        self.errorLabel = CTkLabel(master=window, text=consts.ERROR_LABEL_MSG, text_color=consts.ERROR_LABEL_MSG_COLOR, font=consts.FONT)
        self.entryLogin = CTkEntry(master=window, placeholder_text="Логин")
        self.entryPassword = CTkEntry(master=window, placeholder_text="Пароль", show="*")
        self.entryLogin.pack(padx=20, pady=20)
        self.entryPassword.pack(padx=20, pady=20)
        self.button.pack(padx=20, pady=20)

    def _login(self):
        window = self._window
        login = self.entryLogin.get()
        password = self.entryPassword.get()
        if login and password != "":
            if g_user.authorization(login, password):
                self.clear()
                window.changeContext(MainWindowContext)
            else:
                self.errorLabel.pack(padx=20, pady=20)
        else:
            self.errorLabel.pack(padx=20, pady=20)
