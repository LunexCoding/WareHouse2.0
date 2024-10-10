import re


def convertStringToNumber(number):
    number = number.replace(",", ".")
    match = re.search(r"\d+(\.\d+)?", number)
    
    if match:
        numStr = match.group()
        try:
            num = float(numStr)
            if num.is_integer():
                return int(num)
            return num
        except ValueError:
            try:
                return int(numStr)
            except ValueError:
                return None
    else:
        return None
