from psycopg2 import sql
from postgresql_manager.databases import Databases

class Tables:
    """A static class for managing PostgreSQL tables."""

    @staticmethod
    def exists(database_name: str, table_name: str) -> bool:
        """Checks if a table exists in the specified database."""
        conn = None
        try:
            conn = Databases.connect(database_name)
            if not conn:
                print(f"Failed to connect to database '{database_name}'.")
                return False

            cursor = conn.cursor()
            cursor.execute(sql.SQL("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = %s
                );
            """), [table_name])
            exists = cursor.fetchone()[0]
            cursor.close()
            return exists
        except Exception as e:
            print(f"Error checking existence of table '{table_name}' in '{database_name}': {e}")
            return False
        finally:
            if conn:
                try:
                    conn.close()
                except Exception as close_error:
                    print(f"Error closing connection: {close_error}")

    @staticmethod
    def create(database_name: str, table_name: str) -> bool:
        """
        Creates a new table in the specified database.
        
        :param database_name: Database name.
        :param table_name: Name of the table.
        :param columns: Dictionary where keys are column names and values are PostgreSQL data types.
        :return: True if successful, False otherwise.
        """
        conn = None
        try:
            if Tables.exists(database_name, table_name):
                print(f"Table '{table_name}' already exists in '{database_name}'.")
                return False

            conn = Databases.connect(database_name)
            if not conn:
                print(f"Failed to connect to database '{database_name}'.")
                return False

            cursor = conn.cursor()

            # Create table without columns
            query = sql.SQL("CREATE TABLE {} ();").format(sql.Identifier(table_name))

            cursor.execute(query)
            conn.commit()
            cursor.close()
            print(f"Table '{table_name}' created successfully in '{database_name}'.")
            return True
        except Exception as e:
            print(f"Error creating table '{table_name}' in '{database_name}': {e}")
            return False
        finally:
            if conn:
                try:
                    conn.close()
                except Exception as close_error:
                    print(f"Error closing connection: {close_error}")

    @staticmethod
    def delete(database_name: str, table_name: str) -> bool:
        """Deletes a table from the specified database."""
        conn = None
        try:
            if not Tables.exists(database_name, table_name):
                print(f"Table '{table_name}' does not exist in '{database_name}'.")
                return False

            conn = Databases.connect(database_name)
            if not conn:
                print(f"Failed to connect to database '{database_name}'.")
                return False

            cursor = conn.cursor()
            cursor.execute(sql.SQL("DROP TABLE {};").format(sql.Identifier(table_name)))
            conn.commit()
            cursor.close()
            print(f"Table '{table_name}' deleted successfully from '{database_name}'.")
            return True
        except Exception as e:
            print(f"Error deleting table '{table_name}' from '{database_name}': {e}")
            return False
        finally:
            if conn:
                try:
                    conn.close()
                except Exception as close_error:
                    print(f"Error closing connection: {close_error}")
