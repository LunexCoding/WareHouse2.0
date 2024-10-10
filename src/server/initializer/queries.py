from database.tables import DatabaseTables


class SqlQueries:
    applyingSettings = """PRAGMA foreign_keys = ON"""
    createTableRoles = f"""
        CREATE TABLE IF NOT EXISTS {DatabaseTables.ROLES} (
            `ID` INTEGER PRIMARY KEY,
            `Name` VARCHAR(255)
        );
        """
    createTableUsers = f"""
        CREATE TABLE IF NOT EXISTS {DatabaseTables.USERS} (
            `ID` INTEGER PRIMARY KEY,
            `Login` VARCHAR(255) UNIQUE,
            `Password` VARCHAR(255),
            `RoleID` INTEGER,
            `Fullname` VARCHAR(255),
            FOREIGN KEY (`RoleID`) REFERENCES {DatabaseTables.ROLES}(`ID`)
        );
        """
