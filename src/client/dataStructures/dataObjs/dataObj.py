class DataObj:
    _FIELDS = None
    _INPUT_FIELDS = None
    _EDIT_FIELDS = None
    _GENERATED_FIELDS = None
    _MAIN_INPUT_FIELDS = None

    @classmethod
    def getFields(cls):
        return cls._FIELDS

    @classmethod
    def getInputFields(cls):
        return cls._INPUT_FIELDS

    @classmethod
    def getGeneratedFields(cls):
        return cls._GENERATED_FIELDS

    @classmethod
    def getMainInputFields(cls):
        return cls._MAIN_INPUT_FIELDS

    @classmethod
    def getEditFields(cls):
        return cls._EDIT_FIELDS

    @property
    def data(self):
        return {}

    @property
    def dataForDisplaying(self):
        return {}
