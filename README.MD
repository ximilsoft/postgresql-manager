# PostgreSQL Manager

A simple PostgreSQL management package for handling databases, tables, columns, and rows with ease.

## Features

- Create and manage PostgreSQL databases
- Create and modify tables
- Add, update, and delete columns
- Insert and manage rows
- Easy-to-use API for database operations

## Installation

Install the package using pip:

```bash
pip install postgresql_manager
```

## Importing the Module

```python
from postgresql_manager import Databases, Tables, Columns, Rows
```

## 🚀 Usage

### Databases

#### Check if a Database Exists

```python
database_exists = Databases.exists("mydatabase")
print(f"Database exists: {database_exists}")  # True or False
```

#### Create a Database

```python
database_created = Databases.create("mydatabase")
print(f"Database created: {database_created}")  # True or False
```

#### Delete a Database

```python
database_deleted = Databases.delete("mydatabase")
print(f"Database deleted: {database_deleted}")  # True or False
```

### Tables

#### Check if a Table Exists

```python
table_exists = Tables.exists("users")
print(f"Table exists: {table_exists}")  # True or False
```

#### Create a Table

```python
table_created = Tables.create("users")
print(f"Table created: {table_created}")  # True or False
```

#### Delete a Table

```python
table_deleted = Tables.delete("users")
print(f"Table deleted: {table_deleted}")  # True or False
```

### Columns

#### Check If a Column Exists

```python
column_exists = Columns.exists("mydatabase", "users", "name")
print(f"Column exists: {column_exists}")
```

#### Create a Column

```python
column_created = Columns.create("mydatabase", "users", "id", "INT", True, True)
print(f"Column created: {column_created}")  # True or False
```

#### Delete a Column

```python
column_deleted = Columns.delete("mydatabase", "users", "token")
print(f"Column deleted: {column_deleted}")  # True or False
```

### Rows

#### Check If a Row Exists

```python
row_exists = Rows.exists("mydatabase", "users", 1)
print(f"Row exists: {row_exists}")
```

#### Create a Row

```python
data = {"id": 1, "first_name": "John", "last_name": "Smith"}
Rows.create("mydatabase", "users", data)
```

#### Delete a Row

```python
row_deleted = Rows.delete("mydatabase", "users", 1)
print(f"Row deleted: {row_deleted}")  # True or False
```

## 🤝 Contributing

We welcome contributions! If you’d like to improve this project, follow these steps:

### 1️⃣ Fork the Repository
Click the "Fork" button on GitHub and clone your copy:

```bash
git clone https://github.com/ximilsoft/postgresql_manager.git
cd postgresql_manager
```

### 2️⃣ Create a New Branch

Create a feature branch for your work:

```bash
git checkout -b feature-new-functionality
```

### 3️⃣ Make Changes & Test
Modify the code and test locally.

### 4️⃣ Commit & Push

```bash
git add .
git commit -m "Added a new feature"
git push origin feature-new-functionality
```

### 5️⃣ Submit a Pull Request
Go to GitHub, open a pull request (PR), and describe your changes.

## 📜 License

This project is licensed under the MIT License.

## 📞 Contact

For any issues, open a GitHub issue or reach out via [your email].
