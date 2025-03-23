from psycopg2 import sql
from postgresql_manager.databases import Databases
from postgresql_manager import Manager

class Columns:
    """A static class for managing PostgreSQL table columns."""

    VALID_COLUMN_TYPES = {"INT", "VARCHAR", "TEXT", "BOOLEAN", "DATE", "FLOAT", "SERIAL"}
    """
    VALID_COLUMN_TYPES = {
        "SMALLINT", "INTEGER", "INT", "BIGINT", "DECIMAL", "NUMERIC", "REAL", "DOUBLE PRECISION", "SERIAL", "BIGSERIAL",
        "CHAR", "VARCHAR", "TEXT",
        "DATE", "TIME", "TIMESTAMP", "TIMESTAMPTZ", "INTERVAL",
        "BOOLEAN",
        "UUID",
        "INTEGER[]", "TEXT[]",
        "JSON", "JSONB", "XML",
        "BYTEA", "INET", "CIDR", "MACADDR",
        "POINT", "LINE", "LSEG", "BOX", "PATH", "POLYGON", "CIRCLE"
    }
    """

    @staticmethod
    def exists(database_name: str, table_name: str, column_name: str) -> bool:
        """Checks if a column exists in a table within the specified database."""
        conn = None
        try:
            conn = Databases.connect(database_name)
            if not conn:
                print(f"Failed to connect to database '{database_name}'.")
                return False

            cursor = conn.cursor()
            cursor.execute(sql.SQL("""
                SELECT EXISTS (
                    SELECT 1 FROM information_schema.columns
                    WHERE table_name = %s AND column_name = %s
                );
            """), [table_name, column_name])

            exists = cursor.fetchone()[0]
            cursor.close()
            return exists
        except Exception as e:
            if Manager.debug:
                print(f"Error checking existence of column '{column_name}' in table '{table_name}' in '{database_name}': {e}")
            return False
        finally:
            if conn:
                try:
                    conn.close()
                except Exception as close_error:
                    if Manager.debug:
                        print(f"Error closing connection: {close_error}")

    @staticmethod
    def create(database_name: str, table_name: str, columns: list[dict]) -> bool:
        """Adds multiple columns to a table after validating the column types.
        
        Each column should be a dictionary with keys:
        - 'name': Column name (str)
        - 'type': Column type (str, must be in VALID_COLUMN_TYPES)
        - 'is_not_null': (Optional, bool) Default: True
        - 'is_primary': (Optional, bool) Default: False
        - 'comment': (Optional, str) Default: None
        """
        if not columns:
            if Manager.debug:
                print("No data provided for insertion.")
            return False

        conn = None
        try:
            conn = Databases.connect(database_name)
            if not conn:
                if Manager.debug:
                    print(f"Failed to connect to database '{database_name}'.")
                return False

            cursor = conn.cursor()

            for column in columns:
                name = column.get("name")
                col_type = column.get("type", "").upper()
                is_not_null = column.get("is_not_null", True)
                is_primary = column.get("is_primary", False)
                comment = column.get("comment")

                if col_type not in Columns.VALID_COLUMN_TYPES:
                    if Manager.debug:
                        print(f"Invalid column type '{col_type}' for column '{name}'.")
                    continue  # Skip invalid column types

                # Build constraints
                constraints = []
                if is_primary:
                    constraints.append("PRIMARY KEY")
                if is_not_null:
                    constraints.append("NOT NULL")

                column_definition = f"{col_type} {' '.join(constraints)}" if constraints else col_type

                # Add column to the table
                query = sql.SQL("ALTER TABLE {} ADD COLUMN {} {};").format(
                    sql.Identifier(table_name),
                    sql.Identifier(name),
                    sql.SQL(column_definition)
                )
                cursor.execute(query)

                # Add comment if provided
                if comment:
                    comment_query = sql.SQL("COMMENT ON COLUMN {}.{} IS %s;").format(
                        sql.Identifier(table_name),
                        sql.Identifier(name)
                    )
                    cursor.execute(comment_query, (comment,))

                if Manager.debug:
                    print(f"Column '{name}' added successfully to table '{table_name}' in database '{database_name}'.")

            conn.commit()
            cursor.close()
            return True
        except Exception as e:
            if Manager.debug:
                print(f"Error adding columns to table '{table_name}' in '{database_name}': {e}")
            return False
        finally:
            if conn:
                try:
                    conn.close()
                except Exception as close_error:
                    if Manager.debug:
                        print(f"Error closing connection: {close_error}")

    @staticmethod
    def delete(database_name: str, table_name: str, column_name: str) -> bool:
        """Deletes a column from a table."""
        conn = None
        try:
            conn = Databases.connect(database_name)
            if not conn:
                print(f"Failed to connect to database '{database_name}'.")
                return False

            cursor = conn.cursor()
            cursor.execute(sql.SQL("ALTER TABLE {} DROP COLUMN {};").format(
                sql.Identifier(table_name),
                sql.Identifier(column_name)
            ))
            conn.commit()
            cursor.close()
            if Manager.debug:
                print(f"Column '{column_name}' deleted successfully from table '{table_name}' in '{database_name}'.")
            return True
        except Exception as e:
            if Manager.debug:
                print(f"Error deleting column '{column_name}' from table '{table_name}' in '{database_name}': {e}")
            return False
        finally:
            if conn:
                try:
                    conn.close()
                except Exception as close_error:
                    if Manager.debug:
                        print(f"Error closing connection: {close_error}")
