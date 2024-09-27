from customtkinter import CTkButton, CTkFrame, Y

from .consts import Constants
from .pages import Pages
from .context import Context
from ui.widgets import PageNameWidget, UserInfoWidget

from user import g_user
from commands.roles import RolesInt, Roles


class MainWindowContext(Context):
    def __init__(self, window, data):
        super().__init__(window, data)
        window.title(Constants.PAGE_MAIN)
        self.frame = CTkFrame(window)

        UserInfoWidget(self.frame)
        PageNameWidget(self.frame, Constants.PAGE_MAIN)

        self.buttonFrame = CTkFrame(self.frame)
        self.buttonOpenUsersContext = CTkButton(self.buttonFrame, text=Constants.PAGE_USERS, font=Constants.FONT, command=self._onButtonOpenUsersContextClicked)

        if g_user.role in [Roles.getRole(RolesInt.ADMIN)]:
            self.buttonOpenUsersContext.grid(row=0, column=1, padx=10, pady=10)
        self.buttonFrame.grid(row=0, column=1, padx=10, pady=10)

        self.exitFrame = CTkFrame(self.frame)
        self.buttonExit = CTkButton(self.exitFrame, text=Constants.BUTTON_EXIT, font=Constants.FONT, command=self._onButtonExit)
        self.buttonExit.pack(padx=10, pady=10)
        self.exitFrame.grid(row=0, column=4, padx=10, pady=10)

        self.frame.pack(fill=Y, padx=10, pady=10)

    def _onButtonOpenUsersContextClicked(self):
        window = self._window
        self.clear()
        context = Pages.USERS
        window.changeContext(
            context.context,
            {
                "name": Constants.PAGE_USERS,
                "book": context.book
            }
        )

    def _onButtonExit(self):
        self._window.close()
