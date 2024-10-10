import json


class VALUE_TYPE:
    NONE = 0
    INT = 1
    STRING = 2
    FLOAT = 3
    LIST = 4


class BaseCommand:
    COMMAND_NAME = None

    def __init__(self):
        self.msgHelp = None
        self._allowedFlags = {}
        self._argsWithoutFlagsOrder = []

    def execute(self, **kwargs):
        assert False

    def _getArgs(self, argsline):
        args = argsline.split()
        commandArgs = {}
        last = None
        flags = iter(self._argsWithoutFlagsOrder)
        for arg in args:
            try:
                if last is None:
                    if arg in self._allowedFlags:
                        commandArgs[arg] = None
                        if self._allowedFlags[arg] != VALUE_TYPE.NONE:
                            last = arg
                    else:
                        if "-" in arg:
                            commandArgs[arg] = None
                            last = arg
                        else:
                            last = next(flags)
                            if '[' in arg:
                                arg = arg.replace("[", "").replace("]", "").split(",")
                                commandArgs[last] = arg
                            else:
                                commandArgs[last] = self._convertValue(last, arg)
                            last = None
                else:
                    if '[' in arg:
                        arg = arg.replace("[", "").replace("]", "").split(",")
                        commandArgs[last] = arg
                    else:
                        if "-" in arg:
                            commandArgs[arg] = None
                            last = arg
                        else:
                            commandArgs[last] = self._convertValue(last, arg)
                            last = None
            except StopIteration:
                break
        return commandArgs
    
    def _validateArgs(self, specificArgs=None, baseArgs=None, **kwargs):
        allMissingArgs = []

        missingBaseArgs = self._checkArgs(baseArgs, **kwargs)
        if missingBaseArgs is not None:
            allMissingArgs.extend(missingBaseArgs)

        specificArgs = specificArgs or []
        missingSpecificArgs = self._checkArgs(specificArgs, **kwargs)
        if missingSpecificArgs is not None:
            allMissingArgs.extend(missingSpecificArgs)

        if allMissingArgs:
            return False, allMissingArgs

        return True, None

    def _checkArgs(self, requiredArgs, **kwargs):
        missingArgs = [arg for arg in requiredArgs if kwargs.get(arg) is None]
        if missingArgs:
            return missingArgs
        return None

    def _convertValue(self, flag, arg):
        if not flag in self._allowedFlags:
            return arg
        
        valueType = self._allowedFlags[flag]
        if valueType == VALUE_TYPE.INT:
            return int(arg)
        if valueType == VALUE_TYPE.FLOAT:
            return float(arg)
        if VALUE_TYPE == VALUE_TYPE.LIST:
            return json.loads(arg)
        return arg

    def _checkFlags(self, args):
        invalidFlags = [flag for flag in args if flag not in self._allowedFlags]
        if invalidFlags:
            return False
        missingFlags = [flag for flag in self._allowedFlags if args.get(flag) is None]
        if missingFlags:
            return False
        return True
