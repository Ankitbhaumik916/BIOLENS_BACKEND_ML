import mysql.connector

# Step 1: Connect to the MySQL database
try:
    connection = mysql.connector.connect(
        host="localhost",  # Update with your host (localhost, AWS, etc.)
        user="root",       # Update with your MySQL username
        password="KAERMORHEN2311",  # Update with your MySQL password
        database="nutrition_db"  # Replace with your database name
    )

    # Step 2: Create a cursor object to interact with MySQL
    cursor = connection.cursor()

    # Step 3: Create a table if not exists
    create_table_query = """
    CREATE TABLE IF NOT EXISTS pie (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL UNIQUE,
        phone_no VARCHAR(15) NOT NULL UNIQUE,
        age INT,
        gender VARCHAR(10),
        height FLOAT,
        weight FLOAT,
        password VARCHAR(255) NOT NULL
    );
    """

    cursor.execute(create_table_query)
    print("Table created successfully!")

except mysql.connector.Error as err:
    print(f"Error: {err}")
finally:
    # Close the connection to the database
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed.")

# Function to confirm password
def confirm_password(password, confirm_password):
    return password == confirm_password

# Collect user inputs
name = input("Enter your name: ")
email = input("Enter your email: ")
phone_no = input("Enter your phone number: ")
age = int(input("Enter your age: "))
gender = input("Enter your gender (Male/Female/Other): ")
height = float(input("Enter your height (in meters): "))
weight = float(input("Enter your weight (in kg): "))
password = input("Enter your password: ")
confirm_password_input = input("Confirm your password: ")

# Check if passwords match
if confirm_password(password, confirm_password_input):
    try:
        # Step 1: Connect to MySQL database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="KAERMORHEN2311",  # Update with your MySQL password
            database="nutrition_db"  # Update with your database name
        )

        cursor = connection.cursor()

        # Step 2: Insert user data into MySQL table
        insert_user_query = """
        INSERT INTO pie (name, email, phone_no, age, gender, height, weight, password)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """
        user_data = (name, email, phone_no, age, gender, height, weight, password)

        cursor.execute(insert_user_query, user_data)
        connection.commit()

        print("User added successfully!")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed.")
else:
    print("Passwords do not match! Please try again.")
