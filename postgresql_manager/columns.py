from psycopg2 import sql
from postgresql_manager.databases import Databases

class Columns:
    """A static class for managing PostgreSQL table columns."""

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
            print(f"Error checking existence of column '{column_name}' in table '{table_name}' in '{database_name}': {e}")
            return False
        finally:
            if conn:
                try:
                    conn.close()
                except Exception as close_error:
                    print(f"Error closing connection: {close_error}")

    @staticmethod
    def create(database_name: str, table_name: str, column_name: str, column_type: str, is_not_null: bool = True, is_primary: bool = False, comment: str = None) -> bool:
        """Adds a new column to a table after validating the column type. Supports PRIMARY KEY, NOT NULL constraints, and column comments."""
        
        if column_type.upper() not in Columns.VALID_COLUMN_TYPES:
            print(f"Invalid column type '{column_type}'.")
            return False

        conn = None
        try:
            conn = Databases.connect(database_name)
            if not conn:
                print(f"Failed to connect to database '{database_name}'.")
                return False

            cursor = conn.cursor()

            # Build column definition with constraints
            constraints = []
            if is_primary:
                constraints.append("PRIMARY KEY")
            
            if is_not_null:
                constraints.append("NOT NULL")
            
            column_definition = f"{column_type} {' '.join(constraints)}" if constraints else column_type

            # Add column to the table
            query = sql.SQL("ALTER TABLE {} ADD COLUMN {} {};").format(
                sql.Identifier(table_name),
                sql.Identifier(column_name),
                sql.SQL(column_definition)
            )
            cursor.execute(query)

            # Add comment to column if provided
            if comment:
                comment_query = sql.SQL("COMMENT ON COLUMN {}.{} IS %s;").format(
                    sql.Identifier(table_name),
                    sql.Identifier(column_name)
                )
                cursor.execute(comment_query, (comment,))

            conn.commit()
            cursor.close()
            print(f"Column '{column_name}' added successfully to table '{table_name}' in database '{database_name}'.")
            if comment:
                print(f"Comment added: {comment}")
            return True
        except Exception as e:
            print(f"Error adding column '{column_name}' to table '{table_name}' in '{database_name}': {e}")
            return False
        finally:
            if conn:
                try:
                    conn.close()
                except Exception as close_error:
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
            print(f"Column '{column_name}' deleted successfully from table '{table_name}' in '{database_name}'.")
            return True
        except Exception as e:
            print(f"Error deleting column '{column_name}' from table '{table_name}' in '{database_name}': {e}")
            return False
        finally:
            if conn:
                try:
                    conn.close()
                except Exception as close_error:
                    print(f"Error closing connection: {close_error}")
