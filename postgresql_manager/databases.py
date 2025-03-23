import psycopg2
from psycopg2 import sql, OperationalError

class Databases:
    """A static class for managing PostgreSQL database operations."""

    db_name = "postgres"
    user_name = "postgres"
    password = "newpassword"
    host = "localhost"
    port = "5432"

    @staticmethod
    def config(db_name, user_name, password, host, port) -> bool:
        """Configures the database connection parameters."""
        if not all([db_name, user_name, password, host, port]):
            print("All parameters must be provided.")
            return False

        Databases.db_name = db_name
        Databases.user_name = user_name
        Databases.password = password
        Databases.host = host
        Databases.port = port

        print("Database configuration updated successfully.")
        return True

    @staticmethod
    def exists(db_name=None) -> bool:
        """Checks if a PostgreSQL database exists."""
        
        if not all([Databases.user_name, Databases.password, Databases.host, Databases.port]):
            print("Database connection parameters are not set.")
            return False
        
        db_name = db_name or Databases.db_name
        conn = None
        try:
            conn = psycopg2.connect(
                db_name=db_name,
                user=Databases.user_name,
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
    def create(db_name=None) -> bool:
        """Creates a new PostgreSQL database if it does not exist."""
        
        db_name = db_name or Databases.db_name
        conn = None
        try:
            if Databases.exists(db_name):
                print(f"Database '{db_name}' already exists.")
                return False
            
            conn = psycopg2.connect(
                db_name=Databases.db_name,  # Connect to default database to create a new one
                user=Databases.user_name,
                password=Databases.password,
                host=Databases.host,
                port=Databases.port
            )
            conn.autocommit = True
            cursor = conn.cursor()
            cursor.execute(sql.SQL("CREATE DATABASE {};" ).format(sql.Identifier(db_name)))
            cursor.close()
            print(f"Database '{db_name}' created successfully.")
            return True
        except Exception as e:
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
        
        db_name = db_name or Databases.db_name
        try:
            conn = psycopg2.connect(
                db_name=db_name,
                user=Databases.user_name,
                password=Databases.password,
                host=Databases.host,
                port=Databases.port
            )
            return conn
        except Exception as e:
            print(f"Error connecting to database '{db_name}': {e}")
            return None

    @staticmethod
    def delete(db_name=None) -> bool:
        """Deletes a PostgreSQL database if it exists, ensuring no active connections."""

        db_name = db_name or Databases.db_name
        conn = None
        try:
            if not Databases.exists(db_name):
                print(f"Database '{db_name}' does not exist.")
                return False

            # Connect to the default database to execute termination queries
            conn = psycopg2.connect(
                db_name="postgres",  # Must connect to a different DB to drop the target one
                user=Databases.user_name,
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
            """), [db_name])

            # Drop the database after terminating connections
            cursor.execute(sql.SQL("DROP DATABASE {};").format(sql.Identifier(db_name)))
            cursor.close()
            print(f"Database '{db_name}' deleted successfully.")
            return True
        except Exception as e:
            print(f"Error deleting database '{db_name}': {e}")
            return False
        finally:
            if conn:
                try:
                    conn.close()
                except Exception as close_error:
                    print(f"Error closing connection: {close_error}")
