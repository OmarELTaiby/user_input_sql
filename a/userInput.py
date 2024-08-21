import json
import pyodbc
import os


FILE_PATH = 'user_data.json'
SERVER = input("Enter server name")
DATABASE = 'UserDatabase'
USERNAME = input("Enter user name")
PASSWORD = input("Enter password ")

# Function to initialize the JSON file if it doesn't exist
def initialize_file(file_path):
    """Initialize the file with an empty JSON object if it doesn't exist."""
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            json.dump({}, file)

# Function to load JSON data from a file
def load_data(file_path):
    """Load JSON data from a file. If the file is empty or contains invalid JSON, initialize it."""
    initialize_file(file_path)
    with open(file_path, 'r') as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            # Handle the case where JSON is invalid
            print("File contains invalid JSON. Starting with an empty data structure.")
            return {}

# Function to save JSON data to a file
def save_data(file_path, data):
    """Save the JSON data to the file."""
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

# Function to create a connection to the SQL database
def create_connection(server, database, username, password):
    """Establish a connection to the SQL database."""
    try:
        connection_string = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={server};"
            f"DATABASE={database};"
            f"UID={username};"
            f"PWD={password}"
        )
        conn = pyodbc.connect(connection_string)
        print("Connection successful!")
        return conn
    except pyodbc.Error as e:
        print(f"An error occurred while connecting to the database: {e}")
        return None

# Function to check if a user ID exists in the SQL database
def check_user_id_exists(conn, user_id):
    """Check if the User ID already exists in the SQL database."""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Users WHERE user_id = ?", user_id)
        count = cursor.fetchone()[0]
        return count > 0
    except pyodbc.Error as e:
        print(f"Error checking User ID existence: {e}")
        return False

# Function to insert user data into the SQL database
def insert_user_data(conn, user_info):
    """Insert user data into the SQL database."""
    try:
        cursor = conn.cursor()
        for user_id, details in user_info.items():
            if check_user_id_exists(conn, user_id):
                print(f"ID {user_id} already exists. Skipping insertion.")
                continue
            
            cursor.execute('''
            INSERT INTO Users (user_id, first_name, last_name, age, gender, year_of_birth)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', 
            (user_id, details["First Name"], details["Last Name"], details["Age"], details["Gender"], details["Year of Birth"]))
        
        conn.commit()
    except pyodbc.Error as e:
        print(f"Error inserting user data: {e}")
    finally:
        cursor.close()

# Function to retrieve data from the SQL database
def retrieve_data(conn, user_id=None):
    """Retrieve and display data from the SQL database."""
    try:
        cursor = conn.cursor()
        if user_id:
            cursor.execute("SELECT * FROM Users WHERE user_id = ?", user_id)
            rows = cursor.fetchall()
            if rows:
                for row in rows:
                    print(f"User ID: {row.user_id}, First Name: {row.first_name}, Last Name: {row.last_name}, Age: {row.age}, Gender: {row.gender}, Year of Birth: {row.year_of_birth}")
            else:
                print(f"No data found for User ID: {user_id}")
        else:
            cursor.execute("SELECT * FROM Users")
            rows = cursor.fetchall()
            if rows:
                for row in rows:
                    print(f"User ID: {row.user_id}, First Name: {row.first_name}, Last Name: {row.last_name}, Age: {row.age}, Gender: {row.gender}, Year of Birth: {row.year_of_birth}")
            else:
                print("No data found.")
    except pyodbc.Error as e:
        print(f"Error retrieving data: {e}")
    finally:
        cursor.close()

# Function to validate user input
def validate_alpha(input_str):
    """Check if the input string contains only alphabetic characters."""
    return input_str.isalpha()

def validate_gender(gender):
    """Check if the gender is valid."""
    return gender.lower() in ["male", "female", "other"]

def validate_age(age_str):
    """Check if the age is a positive integer."""
    return age_str.isdigit() and int(age_str) > 0

def validate_year_of_birth(year_str):
    """Check if the year of birth is a four-digit number and the user is at least 18 years old."""
    return year_str.isdigit() and 1900 <= int(year_str) <= 2024

def get_validated_input(prompt, validation_func, error_message):
    """Prompt the user for input until valid data is provided."""
    while True:
        user_input = input(prompt)
        if validation_func(user_input):
            return user_input
        else:
            print(error_message)

# Function to collect user data
def collect_user_data():
    """Collect user data with validation."""
    user_info = {}

    user_id = get_validated_input(
        "Enter your User ID (3 numeric characters): ",
        lambda x: x.isdigit() and len(x) == 3,
        "User ID should be exactly 3 numeric characters."
    )

    first_name = get_validated_input(
        "Enter first name: ",
        validate_alpha,
        "First name should only contain letters."
    )

    last_name = get_validated_input(
        "Enter last name: ",
        validate_alpha,
        "Last name should only contain letters."
    )

    age = get_validated_input(
        "Enter your age: ",
        validate_age,
        "Age must be a positive integer."
    )

    gender = get_validated_input(
        "Enter gender (male/female/other): ",
        validate_gender,
        "Gender must be 'male', 'female', or 'other'."
    )

    year_of_birth = get_validated_input(
        "Enter your year of birth: ",
        validate_year_of_birth,
        "Year of birth must be a four-digit number and the user must be at least 18 years old."
    )

    user_info[user_id] = {
        "First Name": first_name,
        "Last Name": last_name,
        "Age": int(age),
        "Gender": gender,
        "Year of Birth": int(year_of_birth)
    }

    return user_info

# Main function
def main():
    """Main function to run the program."""
    # Load existing data
    data = load_data(FILE_PATH)

    # Collect new user data
    new_user_data = collect_user_data()

    # Save the new user data to the JSON file
    data.update(new_user_data)
    save_data(FILE_PATH, data)

    # Connect to SQL database
    conn = create_connection(SERVER, DATABASE, USERNAME, PASSWORD)
    if conn:
        # Insert user data into SQL database
        insert_user_data(conn, new_user_data)

        # Retrieve and display data
        choice = input("Would you like to display all records or search by User ID? (all/search): ").strip().lower()
        if choice == "all":
            retrieve_data(conn)
        elif choice == "search":
            user_id = input("Enter User ID to search: ")
            retrieve_data(conn, user_id)
        else:
            print("Invalid choice.")
        
        conn.close()

if __name__ == "__main__":
    main()
