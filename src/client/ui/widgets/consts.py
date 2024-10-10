from customtkinter import CTkEntry, CTkComboBox


class WidgetConstants:
    ENTRY = CTkEntry
    COMBOBOX = CTkComboBox

    @classmethod
    def getWidgetClass(cls, widget):
        if widget in (cls.ENTRY, cls.COMBOBOX):
            return widget
        return None
