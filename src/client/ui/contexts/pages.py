from collections import namedtuple

from .pageDataObjContext import PageDataObjContext
from dataStructures.referenceBook import g_usersBook


PAGE = namedtuple("CONTEXT", ["context", "book"])


class Pages:
    USERS = PAGE(PageDataObjContext, g_usersBook)
