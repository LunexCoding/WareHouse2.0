import re


class ProcessConditions:
    @staticmethod
    def process(conditions, columns):
        processedConditions = []

        for condition in conditions:
            for column in columns:
                if column in condition:
                    condition = re.sub(rf'\b{re.escape(column)}\b', f" {column} ", condition)
                    condition = re.sub(r'(?<!<|>|!|=)(=)(?!<|>|!|=)', r' \1 ', condition)
                    condition = re.sub(r'\s*([<>]=?|!=|==)\s*', r' \1 ', condition)
                    condition = re.sub(r'\s+', ' ', condition)
                    condition = condition.strip()
            processedConditions.append(condition)

        if len(processedConditions) == 1:
            processedConditions = "".join(processedConditions)
        return processedConditions
