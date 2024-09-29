from .accessLevel import AccessLevel
from .command import BaseCommand, VALUE_TYPE
from .processConditions import ProcessConditions
import commands.consts as consts

from dataStructures.referenceBook import g_referenceBooks

import network.commands as networkCMD
from network.roles import Roles
from network.status import CommandStatus
from network.tools.dateConverter import convertDateToTimestamp, convertTimestampToDate

from common.logger import logger

_log = logger.getLogger(__name__)


class ClientCommand(BaseCommand):
    def __init__(self):
        super().__init__()
        self.isAuthorizedLevel = False
        self.requiredAccessLevel = AccessLevel.USER

    def _checkAccessLevel(self, clientRole):
        return True if clientRole >= self.requiredAccessLevel else False

    def _checkAuthorizedLevel(self, clientAuthorization):
        return True if clientAuthorization == self.isAuthorizedLevel else False

    def _checkExecutionPermission(self, client):
        if client is None:
            return CommandStatus.FAILED, consts.CLIENT_NOT_ACCEPTED_MDG
        if not self._checkAccessLevel(client.role):
            return CommandStatus.FAILED, consts.ACCESS_ERROR_MSG
        if not self._checkAuthorizedLevel(client.isAuthorized):
            return CommandStatus.FAILED, consts.CLIENT_IS_NOT_AUTHORIZED_MSG
        return CommandStatus.EXECUTED, True


class Authorization(ClientCommand):
    COMMAND_NAME = networkCMD.COMMAND_AUTHORIZATION

    def __init__(self):
        super().__init__()
        self.msgHelp = None
        self._allowedFlags = {
            "-l": VALUE_TYPE.STRING,
            "-p": VALUE_TYPE.STRING
        }
        self._argsWithoutFlagsOrder = ["-l", "-p"]
        self.isAuthorizedLevel = False
        self.requiredAccessLevel = AccessLevel.GUEST

    def execute(self, client=None, commandArgs=None):
        args = self._getArgs(commandArgs)
        if self._checkFlags(args):

            executionPermission = self._checkExecutionPermission(client)
            if executionPermission[0] == CommandStatus.EXECUTED:

                referenceBook = [book for book in g_referenceBooks if book.table == consts.TABLE_FOR_AUTHORZATION][0]
                login = args["-l"]
                password = args["-p"]

                user = self._getUser(login, password, referenceBook)
                if user is not None:
                    role = self._getRole(user)
                    user["Role"] = Roles.getRoleStatus(role)
                    client.authorization(user)
                    del user["Login"]
                    del user["Password"]
                    del user["RoleID"]
                    _log.debug(f"Client is authorized -> ID<{user['ID']}>, fullname: {user['Fullname']}")
                    return CommandStatus.EXECUTED, [user]

                return CommandStatus.FAILED, consts.USER_NOT_FOUND_MSG
            return executionPermission

        return CommandStatus.FAILED, consts.AUTHORIZATION_COMMAND_FAILED_MSG

    @staticmethod
    def _getUser(login, password, referenceBook):
        condition = f"Login='{login}'|Password='{password}'"
        processedCondition = ProcessConditions.process(condition.split("|"), referenceBook.columns)
        user = referenceBook.searchRowByParams(processedCondition)
        if user:
            return user
        return None

    @staticmethod
    def _getRole(user):
        referenceBook = [book for book in g_referenceBooks if book.table == consts.TABLE_ROLES][0]
        roleID = user['RoleID']
        condition = f"ID={roleID}"
        processedCondition = ProcessConditions.process(condition.split("|"), referenceBook.columns)
        role = referenceBook.searchRowByParams(processedCondition)["Name"]
        return role


class SearchRows(ClientCommand):
    COMMAND_NAME = networkCMD.COMMAND_SEARCH

    def __init__(self):
        super().__init__()
        self.msgHelp = None
        self._allowedFlags = {
            "-t": VALUE_TYPE.STRING,
            "-c": VALUE_TYPE.STRING
        }
        self._argsWithoutFlagsOrder = ["-t", "-c"]
        self.isAuthorizedLevel = True
        self.requiredAccessLevel = AccessLevel.USER

    def execute(self, client=None, commandArgs=None):
        args = self._getArgs(commandArgs)
        if self._checkFlags(args):

            executionPermission = self._checkExecutionPermission(client)
            if executionPermission[0] == CommandStatus.EXECUTED:

                table = args["-t"]
                referenceBook = [book for book in g_referenceBooks if book.table == table][0]
                conditionString = args["-c"].replace(networkCMD.SERVICE_SYMBOL_FOR_ARGS, " ")
                conditions = ProcessConditions.process(conditionString.split("|"), referenceBook.columns)
                data = referenceBook.searchRowByParams(conditions)
                if consts.CREATION_DATE_FIELD in data:
                    data["CreationDate"] = convertDateToTimestamp(data["CreationDate"])
                return CommandStatus.EXECUTED, [data]

            return executionPermission
        return CommandStatus.FAILED, None


class AddRow(ClientCommand):
    COMMAND_NAME = networkCMD.COMMAND_ADD

    def __init__(self):
        super().__init__()
        self.msgHelp = None
        self._allowedFlags = {
            "-c": VALUE_TYPE.LIST,
            "-v": VALUE_TYPE.LIST,
            "-t": VALUE_TYPE.STRING
        }
        self._argsWithoutFlagsOrder = ["-c", "-v", "-t"]
        self.isAuthorizedLevel = True
        self.requiredAccessLevel = AccessLevel.USER

    def execute(self, client=None, commandArgs=None):
        args = self._getArgs(commandArgs)
        if self._checkFlags(args):

            executionPermission = self._checkExecutionPermission(client)
            if executionPermission[0] == CommandStatus.EXECUTED:

                table = args["-t"]
                referenceBook = [book for book in g_referenceBooks if book.table == table][0]
                columns = args["-c"]
                if len(columns) == 1 and columns[0] == "*":
                    columns = referenceBook.columnsForInsertion.copy()
                values = args["-v"]

                row = dict(zip(columns, values))
                if consts.CREATION_DATE_FIELD in columns:
                    row["CreationDate"] = convertTimestampToDate(row["CreationDate"])
                rowID = referenceBook.addRow(row)
                if rowID is not None:
                    status, result = SearchRows().execute(client, f"{table} ID={rowID}")
                    if status == CommandStatus.EXECUTED:
                        if consts.CREATION_DATE_FIELD in columns:
                            result["CreationDate"] = convertDateToTimestamp(result["CreationDate"])
                        return CommandStatus.EXECUTED, [result]

                    return CommandStatus.FAILED, None
                return CommandStatus.FAILED, None
            return executionPermission

        return CommandStatus.FAILED, None


class LoadRows(ClientCommand):
    COMMAND_NAME = networkCMD.COMMAND_LOAD

    def __init__(self):
        super().__init__()
        self.msgHelp = None
        self._allowedFlags = {
            "-t": VALUE_TYPE.STRING
        }
        self._argsWithoutFlagsOrder = ["-t"]
        self.isAuthorizedLevel = True
        self.requiredAccessLevel = AccessLevel.USER

    def execute(self, client=None, commandArgs=None):
        args = self._getArgs(commandArgs)
        if self._checkFlags(args):

            executionPermission = self._checkExecutionPermission(client)
            if executionPermission[0] == CommandStatus.EXECUTED:

                table = args["-t"]
                referenceBook = [book for book in g_referenceBooks if book.table == table][0]
                rows = referenceBook.loadRows(client)
                return CommandStatus.EXECUTED, rows

            return executionPermission
        return CommandStatus.FAILED, consts.AUTHORIZATION_COMMAND_FAILED_MSG


class DeleteRow(ClientCommand):
    COMMAND_NAME = networkCMD.COMMAND_DELETE

    def __init__(self):
        super().__init__()
        self.msgHelp = None
        self._allowedFlags = {
            "-i": VALUE_TYPE.INT,
            "-t": VALUE_TYPE.STRING
        }
        self._argsWithoutFlagsOrder = ["-i", "-t"]
        self.isAuthorizedLevel = True
        self.requiredAccessLevel = AccessLevel.ADMIN

    def execute(self, client=None, commandArgs=None):
        args = self._getArgs(commandArgs)
        if self._checkFlags(args):

            executionPermission = self._checkExecutionPermission(client)
            if executionPermission[0] == CommandStatus.EXECUTED:

                rowID = args["-i"]
                table = args["-t"]
                referenceBook = [book for book in g_referenceBooks if book.table == table][0]
                referenceBook.deleteRow(rowID)
                return CommandStatus.EXECUTED, rowID

            return executionPermission
        return CommandStatus.FAILED, consts.AUTHORIZATION_COMMAND_FAILED_MSG


class UpdateRow(ClientCommand):
    COMMAND_NAME = networkCMD.COMMAND_UPDATE

    def __init__(self):
        super().__init__()
        self.msgHelp = None
        self._allowedFlags = {
            "-t": VALUE_TYPE.STRING,
            "-c": VALUE_TYPE.LIST,
            "-v": VALUE_TYPE.LIST
        }
        self._argsWithoutFlagsOrder = ["-c", "-v", "-t"]
        self.isAuthorizedLevel = True
        self.requiredAccessLevel = AccessLevel.ADMIN

    def execute(self, client=None, commandArgs=None):
        args = self._getArgs(commandArgs)
        if self._checkFlags(args):

            executionPermission = self._checkExecutionPermission(client)
            if executionPermission[0] == CommandStatus.EXECUTED:
                table = args["-t"]
                columns = args["-c"]
                values = [value.replace(networkCMD.SERVICE_SYMBOL_FOR_ARGS, " ") for value in args["-v"]]
                data = dict(zip(columns, values))
                rowID = data["ID"]
                if consts.CREATION_DATE_FIELD in columns:
                    data["CreationDate"] = convertTimestampToDate(data["CreationDate"])
                del data["ID"]
                referenceBook = [book for book in g_referenceBooks if book.table == table][0]
                row = referenceBook.updateRow(rowID, data)
                return CommandStatus.EXECUTED, [row]

            return executionPermission
        return CommandStatus.FAILED, consts.AUTHORIZATION_COMMAND_FAILED_MSG


COMMANDS = {
    SearchRows.COMMAND_NAME: SearchRows,
    AddRow.COMMAND_NAME: AddRow,
    LoadRows.COMMAND_NAME: LoadRows,
    DeleteRow.COMMAND_NAME: DeleteRow,
    UpdateRow.COMMAND_NAME: UpdateRow,
    Authorization.COMMAND_NAME: Authorization
}
