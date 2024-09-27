from customtkinter import CTkFrame, CTkButton, CTkLabel, BOTH

from ui.contexts.popup.consts import Constants
from ui.contexts.context import Context
from ui.contexts.consts import Constants as ContextsConstants
from ui.contexts.popup.consts import DataObjContextType
from ui.widgets.consts import WidgetConstants
from ui.widgets.errorLabel import ErrorLabel

from tools.fieldsGenerator import g_fieldsGenerator


class DataObjContext(Context):
    def __init__(self, window, data):
        super().__init__(window, data)
        self._name = data["name"]
        self._command = data["command"]
        self._contextType = data["contextType"]
        window.title(self._name)

        if self._contextType == DataObjContextType.INFO:
            self._dataObj = data["item"]
            self._requiredColumns = self._dataObj.getEditFields()
            window.geometry(f"{Constants.WINDOW_WIDTH}x{Constants.DEFAULT_FIELD_HEIGHT * (len(self._requiredColumns) + 2)}")
        else:
            self._dataObj = data["dataObj"]
            self._requiredColumns = self._dataObj.getInputFields()
            window.geometry(f"{Constants.WINDOW_WIDTH}x{Constants.DEFAULT_FIELD_HEIGHT * (len(self._requiredColumns) + 2)}")
        self._entries = {}

        window.focus()

        self.frame = CTkFrame(window)
        self.errorLabel = ErrorLabel(
            self.frame,
            text_color=ContextsConstants.ERROR_LABEL_MSG_COLOR, font=Constants.FONT,
            wraplength=Constants.ERROR_LABEL_WRAP
        )

        for field in self._requiredColumns:
            fieldInfo = self._dataObj.getFields()[field]
            CTkLabel(
                self.frame,
                text=fieldInfo["text"],
                font=Constants.FONT
            ).pack(pady=5)
            widget = WidgetConstants.getWidgetClass(fieldInfo["widget"])
            if widget == WidgetConstants.COMBOBOX:
                entry = widget(
                    self.frame,
                    font=Constants.FONT,
                    width=fieldInfo["size"],
                    values=[str(option) for option in fieldInfo["options"]]
                )
                if self._contextType == DataObjContextType.INFO:
                    entry.set(self._dataObj.data[field])
            else:
                entry = widget(
                    self.frame,
                    font=Constants.FONT,
                    width=fieldInfo["size"]
                )
                if self._contextType == DataObjContextType.INFO:
                    entry.insert(0, self._dataObj.data[field])
            entry.pack(pady=5)
            self._entries[field] = entry

        self.buttonSave = CTkButton(self.frame, text="Сохранить", command=self._onSaveButtonClicked)

        self.buttonSave.pack(pady=15)
        self.frame.pack(fill=BOTH, expand=True)

    def _onSaveButtonClicked(self):
        data = self._validate()
        if data is None:
            self.errorLabel.show()
        else:
            self.errorLabel.hide()
            self._command(data)

    def _validate(self):
        entriesData = {column: entry.get() if len(entry.get()) != 0 else None for (column, entry) in self._entries.items()}
        if self._contextType == DataObjContextType.INFO:
            entriesData["ID"] = self._dataObj.data["ID"]
        mainFieldsData = {column: entriesData[column] for column in self._dataObj.getMainInputFields() if column in entriesData}
        print(mainFieldsData)
        namesMainFields = {field: fieldData["text"] for field, fieldData in self._dataObj.getFields().items() if field in self._dataObj.getMainInputFields()}
        if not all(value is not None for value in mainFieldsData.values()):
            missingMainFields = [column for column, value in mainFieldsData.items() if value is None]
            missingMainFieldsNames = ", ".join([namesMainFields[column] for column in missingMainFields])
            self.errorLabel.setText(Constants.ERROR_KEY_FIELDS_EMPTY_MSG.format(missingMainFieldsNames))
            return None

        for column, data in entriesData.items():
            if column in self._requiredColumns:
                expectedType = self._dataObj.getFields()[column].get("type")
                if expectedType:
                    try:
                        entriesData[column] = expectedType(data)
                    except ValueError:
                        self.errorLabel.setText(Constants.ERROR_TYPE_MSG.format(namesMainFields[column], expectedType.__name__))
                        return None

        if self._dataObj.getGeneratedFields():
            fields = g_fieldsGenerator.generateFields(self._dataObj.getGeneratedFields())
            if fields:
                for column, value in fields.items():
                    entriesData[column] = value

        return entriesData
