from psycopg2 import sql
from postgresql_manager.databases import Databases

class Rows:
    """A static class for managing PostgreSQL table rows."""

    @staticmethod
    def exists(database_name: str, table_name: str, row_id: int) -> bool:
        """Checks if a row exists in a table by ID."""
        conn = None
        try:
            conn = Databases.connect(database_name)
            if not conn:
                print(f"Failed to connect to database '{database_name}'.")
                return False

            cursor = conn.cursor()

            query = sql.SQL("SELECT EXISTS(SELECT 1 FROM {} WHERE id = %s);").format(
                sql.Identifier(table_name)
            )

            cursor.execute(query, (row_id,))
            exists = cursor.fetchone()[0]
            cursor.close()
            return exists
        except Exception as e:
            print(f"Error checking existence of row ID '{row_id}' in table '{table_name}' in '{database_name}': {e}")
            return False
        finally:
            if conn:
                try:
                    conn.close()
                except Exception as close_error:
                    print(f"Error closing connection: {close_error}")

    @staticmethod
    def create(database_name: str, table_name: str, data: dict) -> bool:
        """
        Inserts a new row into the table.

        :param database_name: Name of the database.
        :param table_name: Name of the table.
        :param data: Dictionary containing column names as keys and values to insert.
        :return: True if successful, False otherwise.
        """
        if not data:
            print("No data provided for insertion.")
            return False

        conn = None
        try:
            conn = Databases.connect(database_name)
            if not conn:
                print(f"Failed to connect to database '{database_name}'.")
                return False

            cursor = conn.cursor()

            columns = data.keys()
            values = data.values()

            query = sql.SQL("INSERT INTO {} ({}) VALUES ({}) RETURNING id;").format(
                sql.Identifier(table_name),
                sql.SQL(", ").join(map(sql.Identifier, columns)),
                sql.SQL(", ").join(sql.Placeholder() * len(values))
            )

            cursor.execute(query, tuple(values))
            inserted_id = cursor.fetchone()[0]  # Get the new row's ID
            conn.commit()
            cursor.close()
            print(f"Row inserted successfully into table '{table_name}' in database '{database_name}' with ID {inserted_id}.")
            return True
        except Exception as e:
            print(f"Error inserting row into table '{table_name}' in '{database_name}': {e}")
            return False
        finally:
            if conn:
                try:
                    conn.close()
                except Exception as close_error:
                    print(f"Error closing connection: {close_error}")

    @staticmethod
    def delete(database_name: str, table_name: str, row_id: int) -> bool:
        """
        Deletes a row from a table by its ID.

        :param database_name: Name of the database.
        :param table_name: Name of the table.
        :param row_id: ID of the row to delete.
        :return: True if deleted successfully, False otherwise.
        """
        conn = None
        try:
            conn = Databases.connect(database_name)
            if not conn:
                print(f"Failed to connect to database '{database_name}'.")
                return False

            cursor = conn.cursor()

            query = sql.SQL("DELETE FROM {} WHERE id = %s;").format(
                sql.Identifier(table_name)
            )

            cursor.execute(query, (row_id,))
            conn.commit()
            cursor.close()
            print(f"Row with ID {row_id} deleted successfully from table '{table_name}' in database '{database_name}'.")
            return True
        except Exception as e:
            print(f"Error deleting row with ID {row_id} from table '{table_name}' in '{database_name}': {e}")
            return False
        finally:
            if conn:
                try:
                    conn.close()
                except Exception as close_error:
                    print(f"Error closing connection: {close_error}")
