from datetime import datetime


class _FieldGenerator:
    def __init__(self):
        self._fieldGenerators = {
            "CreationDate": self._date
        }

    def generateFields(self, fields):
        generatedFields = {}
        for field in fields:
            if field in self._fieldGenerators:
                generatedField = self._fieldGenerators[field]()
                generatedFields[field] = generatedField
            else:
                generatedFields[field] = None
        return generatedFields

    def _date(self):
        return datetime.timestamp(datetime.now())


g_fieldsGenerator = _FieldGenerator()
