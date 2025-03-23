import psycopg2
from psycopg2 import sql, OperationalError
from postgresql_manager import Manager

class Databases:
    """A static class for managing PostgreSQL database operations."""

    @staticmethod
    def exists(db_name=None) -> bool:
        """Checks if a PostgreSQL database exists."""
        
        if not all([Manager.user_name, Manager.password, Manager.host, Manager.port]):
            print("Database connection parameters are not set.")
            return False
        
        db_name = db_name or Manager.db_name
        conn = None
        try:
            conn = psycopg2.connect(
                dbname=db_name,
                user=Manager.user_name,
                password=Manager.password,
                host=Manager.host,
                port=Manager.port
            )
            return True
        except OperationalError as e:
            if Manager.debug:
                print(f"Databases.exists() > {e}")
            return False
        finally:
            if conn:
                try:
                    conn.close()
                except Exception as close_error:
                    if Manager.debug:
                        print(f"Error closing connection: {close_error}")

    @staticmethod
    def create(db_name=None) -> bool:
        """Creates a new PostgreSQL database if it does not exist."""

        db_name = db_name or Manager.db_name
        conn = None
        try:
            if Databases.exists(db_name):
                if Manager.debug:
                    print(f"Database '{db_name}' already exists.")
                return False

            # Connect to the default 'postgres' database
            conn = psycopg2.connect(
                dbname="postgres",  # Fixed: Connect to 'postgres' instead of the new DB
                user=Manager.user_name,
                password=Manager.password,
                host=Manager.host,
                port=Manager.port
            )
            conn.autocommit = True
            cursor = conn.cursor()
            cursor.execute(sql.SQL("CREATE DATABASE {};" ).format(sql.Identifier(db_name)))
            cursor.close()
            if Manager.debug:
                print(f"Database '{db_name}' created successfully.")
            return True
        except Exception as e:
            if Manager.debug:
                print(f"Error creating database '{db_name}': {e}")
            return False
        finally:
            if conn:
                try:
                    conn.close()
                except Exception as close_error:
                    print(f"Error closing connection: {close_error}")

    @staticmethod
    def connect(db_name=None):
        """Connects to a PostgreSQL database (defaults to 'postgres' for administrative tasks)."""
        
        db_name = db_name or Manager.db_name
        try:
            conn = psycopg2.connect(
                dbname=db_name,
                user=Manager.user_name,
                password=Manager.password,
                host=Manager.host,
                port=Manager.port
            )
            return conn
        except Exception as e:
            if Manager.debug:
                print(f"Error connecting to database '{db_name}': {e}")
            return None

    @staticmethod
    def delete(db_name=None) -> bool:
        """Deletes a PostgreSQL database if it exists, ensuring no active connections."""

        db_name = db_name or Manager.db_name
        conn = None
        try:
            if not Databases.exists(db_name):
                if Manager.debug:
                    print(f"Database '{db_name}' does not exist.")
                return False

            # Connect to the default database to execute termination queries
            conn = psycopg2.connect(
                dbname="postgres",  # Must connect to a different DB to drop the target one
                user=Manager.user_name,
                password=Manager.password,
                host=Manager.host,
                port=Manager.port
            )
            conn.autocommit = True
            cursor = conn.cursor()

            # Terminate all active connections to the target database
            cursor.execute(sql.SQL("""
                SELECT pg_terminate_backend(pg_stat_activity.pid)
                FROM pg_stat_activity
                WHERE pg_stat_activity.datname = %s AND pid <> pg_backend_pid();
            """), [db_name])

            # Drop the database after terminating connections
            cursor.execute(sql.SQL("DROP DATABASE {};").format(sql.Identifier(db_name)))
            cursor.close()
            if Manager.debug:
                print(f"Database '{db_name}' deleted successfully.")
            return True
        except Exception as e:
            if Manager.debug:
                print(f"Error deleting database '{db_name}': {e}")
            return False
        finally:
            if conn:
                try:
                    conn.close()
                except Exception as close_error:
                    if Manager.debug:
                        print(f"Error closing connection: {close_error}")
