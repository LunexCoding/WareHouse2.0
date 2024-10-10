from network.roles import Roles


class Client:
    def __init__(self, socket, addr):
        self._socket = socket
        self._addr = addr
        self._userID = None
        self._role = Roles.GUEST
        self.isAuthorized = False
        self._fullname = None
        self._offsetDictionary = {}

    def authorization(self, data):
        if isinstance(data, dict):
            self._userID = data["ID"]
            self._role = data["Role"]
            self._fullname = data["Fullname"]
            self.isAuthorized = True
            return True
        return False

    def updateOffset(self, table, offset):
        if table in self._offsetDictionary:
            self._offsetDictionary[table] = self._offsetDictionary[table] + offset
        else:
            self._offsetDictionary[table] = offset

    def getOffset(self, table):
        return self._offsetDictionary.get(table, 0)

    @property
    def socket(self):
        return self._socket

    @property
    def addr(self):
        return self._addr

    @property
    def userID(self):
        return self._userID

    @property
    def fullname(self):
        return self._fullname

    @property
    def role(self):
        return self._role

    def __str__(self):
        return f"Клиент: ID<{self._userID}>, Name<{self._fullname}>"
