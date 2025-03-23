from postgresql_manager import Manager, Databases, Tables, Columns, Rows

# Configure the database
success = Manager.config(
    db_name="my_database",
    user_name="test_user",
    password="test_password",
    host="127.0.0.1",
    port="5432"
)

if success:
    print("Database configuration successful.")
else:
    print("Database configuration failed. Exiting...")
    exit()

# Create a database
database_my_database = Databases.create("my_database")

if database_my_database:
    print("Database created successfully.")
else:
    print("Failed to create database 'my_database'.")
    exit()

# Create a table
table_users = Tables.create("my_database", "users")

if table_users:
    print("Table created successfully.")
else:
    print("Failed to create table 'users'.")
    exit()

# Create a columns
columns_to_add = [
    {"name": "id", "type": "INT", "is_not_null": False, "is_primary": True},
    {"name": "first_name", "type": "VARCHAR", "is_not_null": True},
    {"name": "last_name", "type": "VARCHAR", "is_not_null": True, "comment": "User's last name"}
]
columns = Columns.create("my_database", "users", columns_to_add)

if columns:
    print("Columns created successfully.")
else:
    print("Failed to create one or more columns.")
    exit()

# Create a rows
rows_to_add = [
    {"id": 1, "first_name": "Alice", "last_name": "Smith"},
    {"id": 2, "first_name": "Bob", "last_name": "Johnson"},
    {"id": 3, "first_name": "Charlie", "last_name": "Brown"},
]
row_created = Rows.create("my_database", "users", rows_to_add)

if row_created:
    print("Row created successfully.")
else:
    print("Failed to create row.")
    exit()
