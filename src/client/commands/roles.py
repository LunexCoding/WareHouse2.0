from collections import namedtuple

from network.roles import Roles as RolesInt


ROLE = namedtuple("Role", ["Guest", "User", "Admin"])


class Roles:
    roles = ROLE(RolesInt.GUEST, RolesInt.USER, RolesInt.ADMIN)

    @classmethod
    def getRole(cls, roleStatus):
        try:
            return ROLE._fields[roleStatus]
        except IndexError:
            return ROLE._fields[0]

    @classmethod
    def getRoleByName(cls, roleName):
        roleDict = cls.roles._asdict()
        for role, value in roleDict.items():
            if role == roleName:
                return value
        return None


ROLES_FOR_INPUT = [RolesInt.USER, RolesInt.ADMIN]
