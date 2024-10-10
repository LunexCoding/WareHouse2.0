from config import g_settingsConfig

from database.database import DatabaseConnection
from database.queries import SqlQueries
from database.tables import ColumnsForInsertion, DatabaseTables

import network.commands as networkCMD
from network.tools.dateConverter import convertDateToTimestamp

from common.config import g_baseConfig


class _ReferenceBook:
    def __init__(self, table, databasePath):
        self._table = table
        self._columns = []
        self._columnsForInsertion = []
        self._sampleLimit = g_baseConfig.Database["limit"]
        self._databaseConnection = DatabaseConnection(databasePath)

    def init(self):
        self._columns = self._getTableColumns()
        self._columnsForInsertion = ColumnsForInsertion.getColumns(self._table)

    def _getTableColumns(self):
        with self._databaseConnection as db:
            columns = db.getData(SqlQueries.getTableColumns(self._table), all=True)
        return [column[1] for column in columns]

    def loadRows(self, client):
        clientOffset = client.getOffset(self._table)
        rows = self._loadRowsFromDB(clientOffset)
        if rows:
            client.updateOffset(self._table, len(rows))
            return rows
        return None

    def _loadRowsFromDB(self, clientOffset):
        with self._databaseConnection as db:
            rows = db.getData(
                SqlQueries.selectFromTable(self._table, requestData="*", limit=self._sampleLimit, offset=clientOffset),
                all=True
            )
        result = []
        for row in rows:
            rowData = {}
            for index, column in enumerate(self._columns):
                rowData[column] = convertDateToTimestamp(row[index]) if "Date" in column else row[index]
            result.append(rowData)
        return result

    def addRow(self, row):
        if not self._checkNextRowExists():
            self._addRowToDB(row)
            return self.lastRowID
        return None

    def _addRowToDB(self, row):
        columns = []
        for column in row.keys():
            if column in self._columnsForInsertion:
                columns.append(column)
            row[column] = row[column].replace(networkCMD.SERVICE_SYMBOL_FOR_ARGS, " ")
        with self._databaseConnection as db:
            db.execute(
                SqlQueries.insertIntoTable(self._table, columns),
                data=list([row[column].replace(networkCMD.SERVICE_SYMBOL, " ") for column in columns])
            )

    def _checkNextRowExists(self):
        with self._databaseConnection as db:
            rowID = db.getData(
                SqlQueries.getLastIDFromTable(self._table)
            )
            if rowID is not None:
                nextRowID = db.getData(
                    SqlQueries.selectRowFromTableByID(self._table, rowID[0] + 1)
                )
                return False if nextRowID is None else True
            return False

    def updateRow(self, rowID, data):
        self._updateRowIntoDB(rowID, data)
        row = self.searchRowByParams(f"ID = {rowID}")
        return row

    def _updateRowIntoDB(self, rowID, data):
        idColumn = self._columns[0]
        with self._databaseConnection as db:
            db.execute(
                SqlQueries.updateTable(self._table, idColumn, rowID, **data),
                data=list(data.values())
            )

    def deleteRow(self, rowID):
        self._deleteRowFromDB(rowID)
        return rowID

    def _deleteRowFromDB(self, rowID):
        idColumn = self._columns[0]
        with self._databaseConnection as db:
            db.execute(
                SqlQueries.deleteFromTable(self._table, idColumn, rowID)
            )

    def searchRowByParams(self, filterData, limit=None, offset=None):
        requestData = {
            "condition": filterData,
            "tableColumns": self._columns
        }
        with self._databaseConnection as db:
            rows = db.getData(
                SqlQueries.selectFromTable(self._table, requestData, limit, offset),
                all=True
            )
        result = []
        for row in rows:
            result.append({self._columns[i]: row[i] for i in range(len(self._columns))})
        if len(result) == 1:
            return result[0]
        return result

    @property
    def table(self):
        return self._table

    @property
    def columns(self):
        return self._columns

    @property
    def columnsForInsertion(self):
        return self._columnsForInsertion

    @property
    def lastRowID(self):
        with self._databaseConnection as db:
            return db.getData(
                SqlQueries.getLastIDFromTable(self._table)
            )[0]


class ReferenceBookFactory:
    def __init__(self, databaseFactory):
        self.databaseFactory = databaseFactory

    def createReferenceBook(self, table):
        return _ReferenceBook(table, self.databaseFactory)


g_usersBook = _ReferenceBook(DatabaseTables.USERS, g_settingsConfig.DatabaseSettings["fullPath"])
g_userRolesBook = _ReferenceBook(DatabaseTables.ROLES, g_settingsConfig.DatabaseSettings["fullPath"])

g_referenceBooks = [g_usersBook, g_userRolesBook]
