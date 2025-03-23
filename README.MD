# PostgreSQL Manager

A simple PostgreSQL management package for handling databases, tables, columns, and rows with ease.

## Features

- Create and manage PostgreSQL databases
- Create and modify tables
- Add, update, and delete columns
- Insert and manage rows
- Easy-to-use API for database operations

## Installation

### Install the Package

Install the package using pip:

```bash
pip install postgresql_manager
```

### Import the Package

```python
from postgresql_manager import Manager, Databases, Tables, Columns, Rows
```

### Configure the Database

```python
# Configure the database connection
success = Manager.config(
    db_name="my_database",
    user_name="test_user",
    password="test_password",
    host="127.0.0.1",
    port="5432"
)

# Check if configuration was successful
if success:
    print("Configuration set successfully.")
else:
    print("Failed to set configuration.")
```

## Usage

### Databases

#### Check if a Database Exists

```python
database_exists = Databases.exists("my_database")
print(f"Database exists: {database_exists}") # True or False
```

#### Create a Database

```python
database_created = Databases.create("my_database")
print(f"Database created: {database_created}") # True or False
```

#### Delete a Database

```python
database_deleted = Databases.delete("my_database")
print(f"Database deleted: {database_deleted}") # True or False
```

### Tables

#### Check if a Table Exists

```python
table_exists = Tables.exists("my_database", "users")
print(f"Table exists: {table_exists}") # True or False
```

#### Create a Table

```python
table_created = Tables.create("my_database", "users")
print(f"Table created: {table_created}") # True or False
```

#### Delete a Table

```python
table_deleted = Tables.delete("my_database", "users")
print(f"Table deleted: {table_deleted}") # True or False
```

### Columns

#### Check If a Column Exists

```python
column_exists = Columns.exists("my_database", "users", "name")
print(f"Column exists: {column_exists}") # True or False
```

#### Create a Column

```python
columns_to_add = [
    {"name": "id", "type": "INT", "is_not_null": False, "is_primary": True},
    {"name": "first_name", "type": "VARCHAR", "is_not_null": True},
    {"name": "last_name", "type": "VARCHAR", "is_not_null": True, "comment": "User's last name"}
]
columns = Columns.create("my_database", "users", columns_to_add)
print(f"Columns: {columns}") # True or False
```

#### Delete a Column

```python
column_deleted = Columns.delete("my_database", "users", "token")
print(f"Column deleted: {column_deleted}") # True or False
```

### Rows

#### Check If a Row Exists

```python
row_exists = Rows.exists("my_database", "users", 1)
print(f"Row exists: {row_exists}") # True or False
```

#### Create a Row

```python
rows_to_add = [
    {"id": 1, "first_name": "Alice", "last_name": "Smith"},
    {"id": 2, "first_name": "Bob", "last_name": "Johnson"},
    {"id": 3, "first_name": "Charlie", "last_name": "Brown"},
]
row_created = Rows.create("my_database", "users", rows_to_add)
print(f"Row created: {row_created}") # True or False
```

#### Delete a Row

```python
row_deleted = Rows.delete("my_database", "users", 1)
print(f"Row deleted: {row_deleted}") # True or False
```

## Getting Help

If you have any questions or need assistance, feel free to [open an issue](https://github.com/ximilsoft/postgresql-manager/issues).

## Contributing

We welcome contributions, If you’d like to improve this project, follow these steps:

#### 1. Fork the Repository

Click the "Fork" button on GitHub and clone your copy:

```bash
git clone https://github.com/ximilsoft/postgresql_manager.git
cd postgresql_manager
```

#### 2. Create a New Branch

Create a feature branch for your work:

```bash
git checkout -b feature-new-functionality
```

#### 3. Make Changes & Test

Modify the code and test locally.

#### 4. Commit & Push

```bash
git add .
git commit -m "Added a new feature"
git push origin feature-new-functionality
```

#### 5. Submit a Pull Request

Go to GitHub, open a pull request (PR), and describe your changes.

## 📅 Roadmap

- [x] Add database configuration.
- [ ] Support for multiple databases.
- [ ] Implement additional database operations.
- [ ] Enhance scalability and performance optimization.

## 📜 License

This project is licensed under the MIT License.

## Support

If you find this project helpful, show your support by starring the repository.
