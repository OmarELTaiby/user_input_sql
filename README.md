# User Data Management System

This project is a Python-based user data management system that interacts with a SQL Server database. It allows you to collect user information, store it in a JSON file, and insert it into a SQL database. Additionally, it provides functionality to retrieve and display user data.

## Features

- **User Data Collection**: Gathers user data with validation for fields such as User ID, First Name, Last Name, Age, Gender, and Year of Birth.
- **Data Storage**: Saves user data to a JSON file.
- **SQL Database Integration**: Connects to a SQL Server database, checks for existing user IDs, and inserts new user data.
- **Data Retrieval**: Allows users to retrieve and display all records or search for a specific user by ID.

## Prerequisites

- **Python**: Make sure Python is installed on your system.
- **pyodbc**: Install the `pyodbc` package to connect to SQL Server.
- **SQL Server**: A running instance of SQL Server with the necessary permissions to connect and perform CRUD operations.

## Setup

1. Install the required Python library:
    ```bash
    pip install pyodbc
    ```

2. Ensure you have ODBC Driver 17 for SQL Server installed.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/OmarELTaiby/user_input_sql.git
cd user_input_sql
2. Run the script

3. Follow the prompts to enter your server name, database name, username, and password.







## License
This project is licensed under the MIT License - see the LICENSE file for details.
