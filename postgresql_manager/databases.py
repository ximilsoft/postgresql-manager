import psycopg2
from psycopg2 import sql, OperationalError

class Databases:
    """A static class for managing PostgreSQL database operations."""

    dbname = "postgres"
    user = "postgres"
    password = "newpassword"
    host = "localhost"
    port = "5432"

    @staticmethod
    def exists(dbname=None) -> bool:
        """Checks if a PostgreSQL database exists."""
        
        if not all([Databases.user, Databases.password, Databases.host, Databases.port]):
            print("Database connection parameters are not set.")
            return False
        
        dbname = dbname or Databases.dbname
        conn = None
        try:
            conn = psycopg2.connect(
                dbname=dbname,
                user=Databases.user,
                password=Databases.password,
                host=Databases.host,
                port=Databases.port
            )
            return True
        except OperationalError as e:
            print(f"Databases.exists() > {e}")
            return False
        finally:
            if conn:
                try:
                    conn.close()
                except Exception as close_error:
                    print(f"Error closing connection: {close_error}")

    @staticmethod
    def create(dbname=None) -> bool:
        """Creates a new PostgreSQL database if it does not exist."""
        
        dbname = dbname or Databases.dbname
        conn = None
        try:
            if Databases.exists(dbname):
                print(f"Database '{dbname}' already exists.")
                return False
            
            conn = psycopg2.connect(
                dbname=Databases.dbname,  # Connect to default database to create a new one
                user=Databases.user,
                password=Databases.password,
                host=Databases.host,
                port=Databases.port
            )
            conn.autocommit = True
            cursor = conn.cursor()
            cursor.execute(sql.SQL("CREATE DATABASE {};" ).format(sql.Identifier(dbname)))
            cursor.close()
            print(f"Database '{dbname}' created successfully.")
            return True
        except Exception as e:
            print(f"Error creating database '{dbname}': {e}")
            return False
        finally:
            if conn:
                try:
                    conn.close()
                except Exception as close_error:
                    print(f"Error closing connection: {close_error}")

    @staticmethod
    def connect(dbname=None):
        """Connects to a PostgreSQL database (defaults to 'postgres' for administrative tasks)."""
        
        dbname = dbname or Databases.dbname
        try:
            conn = psycopg2.connect(
                dbname=dbname,
                user=Databases.user,
                password=Databases.password,
                host=Databases.host,
                port=Databases.port
            )
            return conn
        except Exception as e:
            print(f"Error connecting to database '{dbname}': {e}")
            return None

    @staticmethod
    def delete(dbname=None) -> bool:
        """Deletes a PostgreSQL database if it exists, ensuring no active connections."""

        dbname = dbname or Databases.dbname
        conn = None
        try:
            if not Databases.exists(dbname):
                print(f"Database '{dbname}' does not exist.")
                return False

            # Connect to the default database to execute termination queries
            conn = psycopg2.connect(
                dbname="postgres",  # Must connect to a different DB to drop the target one
                user=Databases.user,
                password=Databases.password,
                host=Databases.host,
                port=Databases.port
            )
            conn.autocommit = True
            cursor = conn.cursor()

            # Terminate all active connections to the target database
            cursor.execute(sql.SQL("""
                SELECT pg_terminate_backend(pg_stat_activity.pid)
                FROM pg_stat_activity
                WHERE pg_stat_activity.datname = %s AND pid <> pg_backend_pid();
            """), [dbname])

            # Drop the database after terminating connections
            cursor.execute(sql.SQL("DROP DATABASE {};").format(sql.Identifier(dbname)))
            cursor.close()
            print(f"Database '{dbname}' deleted successfully.")
            return True
        except Exception as e:
            print(f"Error deleting database '{dbname}': {e}")
            return False
        finally:
            if conn:
                try:
                    conn.close()
                except Exception as close_error:
                    print(f"Error closing connection: {close_error}")
