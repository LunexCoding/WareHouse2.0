class SqlQueries:
    @staticmethod
    def getTableColumns(tableName):
        return f"""PRAGMA table_info({tableName})"""

    # DELETE A ROW FROM A TABLE #
    @staticmethod
    def deleteFromTable(tableName, targetElement, targetValue):
        return f"""
        DELETE FROM {tableName}
        WHERE {targetElement}={targetValue}
        """

    # UPDATE A ROW IN A TABLE #
    @staticmethod
    def updateTable(tableName, targetElement, targetValue, **kwargs):
        return f"""
        UPDATE {tableName}
        SET {", ".join([f"{key}=?" for key, value in kwargs.items()])}
        WHERE {targetElement}={targetValue}
        """

    # INSERT A ROW INTO THE REQUIRED TABLE #
    @staticmethod
    def insertIntoTable(tableName, args):
        return f"""
        INSERT OR IGNORE INTO {tableName}
        ({', '.join([char for char in args])})
        VALUES ({', '.join(["?" for char in args])})
        """

    # SELECT ROWS FROM TABLE #
    @staticmethod
    def selectFromTable(tableName, requestData, args=None, limit=None, offset=None):
        if requestData == "*":
            return SqlQueries._selectAllFromTable(tableName, limit, offset)
        if (requestData is not None) and (requestData != "*"):
            if requestData.get("condition", None) is None:
                return SqlQueries._selectFromTableByWhere(tableName, requestData, args, limit, offset)
            return SqlQueries._selectFromTableByCondition(tableName, requestData, limit, offset)
        return SqlQueries._selectFromTableByParams(tableName, args, limit, offset)

    def _selectFromTableByParams(tableName, args, limit, offset):
        query = f"""
           SELECT {', '.join([char for char in args])}
           FROM {tableName}
           """
        if limit is not None:
            query += f"\nLIMIT {limit}"
        if offset is not None:
            query += f"\nOFFSET {offset}"
        return query

    @staticmethod
    def _selectFromTableByWhere(tableName, requestData, args, limit, offset):
        query = f"""
           SELECT {', '.join([char for char in args])}
           FROM {tableName}
           WHERE {' AND '.join([f'{key}="{value}"' for (key, value) in requestData.items()])}
           """
        if limit is not None:
            query += f"\nLIMIT {limit}"
        if offset is not None:
            query += f"\nOFFSET {offset}"
        return query

    @staticmethod
    def _selectAllFromTable(tableName, limit, offset):
        query = f"""
           SELECT * FROM {tableName}
           """
        if limit is not None:
            query += f"\nLIMIT {limit}"
        if offset is not None:
            query += f"\nOFFSET {offset}"
        return query

    @staticmethod
    def _selectFromTableByCondition(tableName, requestData, limit, offset):
        conditions = requestData.get("condition", None)
        tableColumns = requestData.get("tableColumns", None)
        joins = requestData.get("joins", None)
        columns = []
        data = None

        if tableColumns is not None:
            if isinstance(conditions, list):
                conditionsData = []
                for condition in conditions:
                    conditionData = condition.split()
                    for word in conditionData:
                        if word in tableColumns:
                            columns.append(word)
                            conditionData.remove(word)
                    conditionsData.append(" ".join(conditionData))
                data = conditionsData
            else:
                conditionData = conditions.split()
                for word in conditionData:
                    if word in tableColumns:
                        columns.append(word)
                        conditionData.remove(word)
                data = " ".join(conditionData)

        query = f"SELECT * FROM {tableName}"

        if joins is not None:
            for join in joins:
                query += f" JOIN {join} ON {joins[join]}"

        if data is not None:
            if isinstance(data, list):
                if columns:
                    query += " WHERE "
                    for i, condition in enumerate(data):
                        query += f"{columns[i]} {condition}"
                        if i < len(data) - 1:
                            query += " AND "
                else:
                    query += f" WHERE {' AND '.join(data)}"
            else:
                query += f" WHERE {columns[0]} {data}"

        if limit is not None:
            query += f" LIMIT {limit}"
        if offset is not None:
            query += f" OFFSET {offset}"
        return query

    @staticmethod
    def getLastIDFromTable(table):
        query = f"""
            SELECT id FROM {table} ORDER BY id DESC LIMIT 1
        """
        return query

    @staticmethod
    def selectRowFromTableByID(table, rowID):
        query = f"""
        SELECT ID FROM {table} WHERE ID = {rowID}"""
        return query
