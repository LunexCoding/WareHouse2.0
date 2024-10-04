from dataStructures.dataObjs.user import User

import commands.consts as constants
from commands.center import g_commandCenter

import network.commands as networkCMD
from network.commands import Commands as networkCommands
from network.status import CommandStatus
from network.tables import DatabaseTables
from network.tools.dateConverter import convertTimestampToDate, isTimestamp


class _ReferenceBook:
    def __init__(self, table, dataObj):
        self._table = table
        self._rows = []
        self._dataObj = dataObj

    def _processingResponse(self, commandType, commandID, response):
        if response is None:
            return None
        
        commandIDResponse = int(response.pop(0))
        commandStatus = int(response.pop(0))

        if commandID != commandIDResponse and commandStatus != CommandStatus.EXECUTED:
            return None
        
        rowString = " ".join(response)
        rows = rowString.split("|")
        for index, row in enumerate(rows):
            if row == "None":
                return None
            rowData = []
            for value in row.split():
                if isTimestamp(value):
                    rowData.append(convertTimestampToDate(value))
                else:
                    rowData.append(value)
            rowData = [item.replace(networkCMD.SERVICE_SYMBOL_FOR_ARGS, " ") for item in rowData]
            if commandType != networkCMD.COMMAND_DELETE:
                rows[index] = self._dataObj(*rowData)
            else:
                rows = rowData
        return rows

    def loadRows(self):
        COMMAND_NAME = networkCMD.COMMAND_LOAD
        commandID = networkCommands.getCommandByName(COMMAND_NAME, dict(table=self._table))

        response = g_commandCenter.execute(commandID)
        data = self._processingResponse(COMMAND_NAME, commandID, response)
        if data is None:
            return None
        
        newData = []
        for dataObj in data:
            if not self._checkDataObj(dataObj.data["ID"]):
                self._rows.append(dataObj)
                newData.append(dataObj)
        return newData

    def addRow(self, data):
        if data is None:
            return None
        
        COMMAND_NAME = networkCMD.COMMAND_ADD
        commandID = networkCommands.getCommandByName(COMMAND_NAME, dict(table=self._table))
        columns = "[*]"
        values = [",".join([value.replace(" ", networkCMD.SERVICE_SYMBOL_FOR_ARGS) for value in map(str, data.values())])]
        command = constants.DEFAULT_COMMAND_STRING.format(commandID, columns, values).replace("'", "")

        response = g_commandCenter.execute(command)
        data = self._processingResponse(COMMAND_NAME, commandID, response)
        if data is None:
            return None
        
        dataObj = data[0]
        
        self._rows.append(dataObj)
        return dataObj

    def removeRow(self, rowID):
        COMMAND_NAME = networkCMD.COMMAND_DELETE
        commandID = networkCommands.getCommandByName(COMMAND_NAME, dict(table=self._table))
        command = constants.COMMAND_STRING_WITH_TWO_ARGS.format(commandID, rowID)

        response = g_commandCenter.execute(command)
        receivedID = self._processingResponse(COMMAND_NAME, commandID, response)[0]
        if receivedID is None:
            return None
        
        dataObj = self.findDataObjByID(int(receivedID))
        if dataObj is None:
            return None
        
        self._rows.remove(dataObj)
        return receivedID
           
    def updateRow(self, data):
        if data is None:
            return None
        
        COMMAND_NAME = networkCMD.COMMAND_UPDATE
        commandID = networkCommands.getCommandByName(COMMAND_NAME, dict(table=self._table))
        columns = [",".join([column.replace(" ", "") for column in list(data.keys())])]
        values = [",".join([value.replace(" ", networkCMD.SERVICE_SYMBOL_FOR_ARGS) for value in map(str, data.values())])]
        command = constants.DEFAULT_COMMAND_STRING.format(commandID, columns, values).replace("'", "")

        response = g_commandCenter.execute(command)
        dataObj = self._processingResponse(COMMAND_NAME, commandID, response)[0]
        if dataObj is None:
            return None
        
        item = self.findDataObjByID(dataObj.data["ID"])
        if item is None:
            return None

        index = self._rows.index(item)
        self._rows[index] = dataObj
        return dataObj
            
    def _checkDataObj(self, id):
        return any(dataObj.data["ID"] == id for dataObj in self._rows)

    def findDataObjByID(self, id):
        for dataObj in self._rows:
            if dataObj.data["ID"] == id:
                return dataObj
        return None

    @property
    def rows(self):
        return self._rows

    @property
    def dataObj(self):
        return self._dataObj

    @property
    def table(self):
        return self._table


g_usersBook = _ReferenceBook(DatabaseTables.USERS, User)
