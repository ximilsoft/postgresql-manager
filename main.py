from postgresql_manager import Databases, Tables, Columns, Rows

# Example usage
db = Databases.create("mydatabase")
table = Tables.create("mydatabase", "users")
column = Columns.create("mydatabase", "users", "id", "INT", True, True)

# Step 1: Create the database if it doesn’t exist
db = Databases.create("mydatabase")
table = Tables.create("mydatabase", "users")
column_1 = Columns.create("mydatabase", "users", "id", "INT", True, True)
column_2 = Columns.create("mydatabase", "users", "name", "VARCHAR", True)
column_3 = Columns.create("mydatabase", "users", "token", "VARCHAR", False)

data = {"id" :1, "name": "mohammed", "token": "xxxx"}
row = Rows.create("mydatabase", "users", data)

print(f"db: {db}")
print(f"table: {table}")
print(f"column_1: {column_1}")
print(f"column_1: {column_2}")
print(f"column_1: {column_3}")

print(f"row: {column_1}")