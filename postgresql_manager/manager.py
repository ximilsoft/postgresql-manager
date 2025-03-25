import psycopg2
from psycopg2 import sql, OperationalError

class Manager:

    db_name = "postgres"
    user_name = "postgres"
    password = "newpassword"
    host = "localhost"
    port = "5432"
    debug = False
    
    con = None

    @staticmethod
    def start(db_name, user_name, password, host, port, debug=False) -> bool:
        """Configures the database connection parameters."""
        if not all([db_name, user_name, password, host, port]):
            if debug:
                print("All parameters must be provided.")
            return False

        Manager.db_name = db_name
        Manager.user_name = user_name
        Manager.password = password
        Manager.host = host
        Manager.port = port
        Manager.debug = debug

        if debug:
            print("Database configuration updated successfully.")
        return True

    @staticmethod
    def end() -> bool:
        """Closes the database connection if it's open."""
        from postgresql_manager import Databases
        return Databases.disconnect()
