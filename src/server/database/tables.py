from network.tables import DatabaseTables


class ColumnsForInsertion:
    _tableColumns = {
        DatabaseTables.USERS.value: ["Login", "Password", "RoleID", "Fullname"]
    }

    @staticmethod
    def getColumns(tableName):
        return ColumnsForInsertion._tableColumns.get(tableName, [])
