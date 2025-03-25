
from psycopg2 import sql
from postgresql_manager.databases import Databases
from postgresql_manager import Manager

class Rows:
    """A static class for managing PostgreSQL table rows."""

    @staticmethod
    def exists(database_name: str, table_name: str, conditions: dict, logical_operator: str = "AND") -> bool:
        """Checks if a row exists in a table based on dynamic conditions with AND/OR support.
        
        :param database_name: Name of the database.
        :param table_name: Name of the table.
        :param conditions: Dictionary of column-value pairs for filtering.
        :param logical_operator: Logical operator to combine conditions ('AND' or 'OR').
        :return: True if a matching row exists, False otherwise.
        """
        conn = None
        try:
            conn = Databases.connect(database_name)
            if not conn:
                print(f"Failed to connect to database '{database_name}'.")
                return False

            cursor = conn.cursor()

            # Ensure the logical operator is valid
            logical_operator = logical_operator.upper()
            if logical_operator not in ["AND", "OR"]:
                logical_operator = "AND"

            # Build WHERE clause dynamically
            condition_clauses = [sql.SQL("{} = %s").format(sql.Identifier(col)) for col in conditions.keys()]
            where_clause = sql.SQL(f" {logical_operator} ").join(condition_clauses)
            
            query = sql.SQL("SELECT EXISTS(SELECT 1 FROM {} WHERE {});").format(
                sql.Identifier(table_name),
                where_clause
            )

            cursor.execute(query, tuple(conditions.values()))
            exists = cursor.fetchone()[0]
            cursor.close()
            return exists
        except Exception as e:
            if Manager.debug:
                print(f"Error checking existence of row in table '{table_name}' in '{database_name}': {e}")
            return False
        finally:
            if conn:
                try:
                    conn.close()
                except Exception as close_error:
                    if Manager.debug:
                        print(f"Error closing connection: {close_error}")

    @staticmethod
    def list(database_name: str, table_name: str, conditions: dict = None, logical_operator: str = "AND", limit: int = 100) -> list:
        """Retrieves rows from a table based on conditions with AND/OR support and allows operators in conditions.

        :param database_name: Name of the database.
        :param table_name: Name of the table.
        :param conditions: Dictionary where keys are column names (optionally with an operator, e.g., "start_time >")
                           and values are the corresponding filter values.
        :param logical_operator: Logical operator to combine conditions ('AND' or 'OR').
        :param limit: Maximum number of rows to retrieve.
        :return: List of dictionaries representing the rows.
        """
        conn = None
        try:
            conn = Databases.connect(database_name)
            if not conn:
                print(f"Failed to connect to database '{database_name}'.")
                return []

            cursor = conn.cursor()
            base_query = sql.SQL("SELECT * FROM {}").format(sql.Identifier(table_name))

            query_params = []
            where_clause = sql.SQL("")

            if conditions:
                logical_operator = logical_operator.upper()
                if logical_operator not in ["AND", "OR"]:
                    logical_operator = "AND"

                condition_clauses = []
                for col, value in conditions.items():
                    if " " in col:  # Check if an operator is included (e.g., "start_time >")
                        col_name, operator = col.rsplit(" ", 1)
                        operator = operator.strip()
                        if operator not in [">", "<", ">=", "<=", "!=", "="]:
                            continue  # Skip invalid operators
                    else:
                        col_name, operator = col, "="  # Default to '=' operator
                    
                    condition_clauses.append(sql.SQL("{} {} %s").format(sql.Identifier(col_name), sql.SQL(operator)))
                    query_params.append(value)

                where_clause = sql.SQL(" WHERE ") + sql.SQL(f" {logical_operator} ").join(condition_clauses)

            query = base_query + where_clause + sql.SQL(" LIMIT %s")
            query_params.append(limit)

            cursor.execute(query, tuple(query_params))
            columns = [desc[0] for desc in cursor.description]
            rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
            cursor.close()
            return rows

        except Exception as e:
            if Manager.debug:
                print(f"Error retrieving rows from table '{table_name}' in '{database_name}': {e}")
            return []
        finally:
            if conn:
                try:
                    conn.close()
                except Exception as close_error:
                    if Manager.debug:
                        print(f"Error closing connection: {close_error}")

    @staticmethod
    def create(database_name: str, table_name: str, data_list: list) -> bool:
        """
        Inserts multiple rows into the table.

        :param database_name: Name of the database.
        :param table_name: Name of the table.
        :param data_list: List of dictionaries containing column names as keys and values to insert.
        :return: True if successful, False otherwise.
        """
        if not data_list:
            if Manager.debug:
                print("No data provided for insertion.")
            return False

        conn = None
        try:
            conn = Databases.connect(database_name)
            if not conn:
                print(f"Failed to connect to database '{database_name}'.")
                return False

            cursor = conn.cursor()

            # Extract column names from the first dictionary
            columns = list(data_list[0].keys())

            # Create SQL placeholders (%s, %s, ...)
            values_placeholder = sql.SQL(", ").join([sql.Placeholder()] * len(columns))

            # Construct query
            query = sql.SQL("INSERT INTO {} ({}) VALUES ({}) RETURNING id;").format(
                sql.Identifier(table_name),
                sql.SQL(", ").join(map(sql.Identifier, columns)),
                values_placeholder
            )

            inserted_ids = []
            for data in data_list:
                cursor.execute(query, tuple(data.values()))
                inserted_ids.append(cursor.fetchone()[0])  # Get the new row's ID

            conn.commit()
            cursor.close()

            if Manager.debug:
                print(f"{len(data_list)} rows inserted successfully into table '{table_name}' in database '{database_name}'. Inserted IDs: {inserted_ids}")

            return True
        except Exception as e:
            if Manager.debug:
                print(f"Error inserting rows into table '{table_name}' in '{database_name}': {e}")
            return False
        finally:
            if conn:
                try:
                    conn.close()
                except Exception as close_error:
                    if Manager.debug:
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
            if Manager.debug:
                print(f"Row with ID {row_id} deleted successfully from table '{table_name}' in database '{database_name}'.")
            return True
        except Exception as e:
            if Manager.debug:
                print(f"Error deleting row with ID {row_id} from table '{table_name}' in '{database_name}': {e}")
            return False
        finally:
            if conn:
                try:
                    conn.close()
                except Exception as close_error:
                    if Manager.debug:
                        print(f"Error closing connection: {close_error}")

    @staticmethod
    def update(database_name: str, table_name: str, row_id: int, update_data: dict) -> bool:
        """
        Updates a row in the table by its ID.

        :param database_name: Name of the database.
        :param table_name: Name of the table.
        :param row_id: ID of the row to update.
        :param update_data: Dictionary of column-value pairs to update.
        :return: True if updated successfully, False otherwise.
        """
        if not update_data:
            if Manager.debug:
                print("No update data provided.")
            return False

        conn = None
        try:
            conn = Databases.connect(database_name)
            if not conn:
                print(f"Failed to connect to database '{database_name}'.")
                return False

            cursor = conn.cursor()

            # Build SET clause dynamically
            set_clauses = [sql.SQL("{} = %s").format(sql.Identifier(col)) for col in update_data.keys()]
            set_clause = sql.SQL(", ").join(set_clauses)

            query = sql.SQL("UPDATE {} SET {} WHERE id = %s;").format(
                sql.Identifier(table_name),
                set_clause
            )

            cursor.execute(query, tuple(update_data.values()) + (row_id,))
            conn.commit()
            cursor.close()
            
            if Manager.debug:
                print(f"Row with ID {row_id} updated successfully in table '{table_name}' in database '{database_name}'.")

            return True
        except Exception as e:
            if Manager.debug:
                print(f"Error updating row with ID {row_id} in table '{table_name}' in '{database_name}': {e}")
            return False
        finally:
            if conn:
                try:
                    conn.close()
                except Exception as close_error:
                    if Manager.debug:
                        print(f"Error closing connection: {close_error}")
