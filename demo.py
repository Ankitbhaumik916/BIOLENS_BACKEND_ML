import requests
import mysql.connector

# CalorieNinjas API endpoint and API key
url = "https://api.calorieninjas.com/v1/nutrition"
api_key = "sJA5BDqLJ+VReWp6OtRUKQ==YxdNXHxOjRKreUNH"

# MySQL connection details
db_config = {
    'host': 'localhost',       # Replace with your MySQL host
    'user': 'root',            # Replace with your MySQL username
    'password': 'KAERMORHEN2311', # Replace with your MySQL password
    'database': 'nutrition_db'  # The database you created
}

# The food item you want to query
query = input("Enter your meal: ")

# Set up headers including the API key
headers = {
    "X-Api-Key": api_key
}

# Parameters for the GET request (search term)
params = {
    "query": query
}

# Send the GET request to the CalorieNinjas API
response = requests.get(url, headers=headers, params=params)

# Check the response status
if response.status_code == 200:
    data = response.json()

    # Check if 'items' key exists in the response
    if "items" in data:
        # Extract the first item (nutrition data for the queried food)
        food_item = data["items"][0]

        # Connect to the MySQL database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Insert the data into the nutrition_info table
        sql = """
        INSERT INTO nutrition_info (name, calories, serving_size_g, fat_total_g, fat_saturated_g, protein_g, sodium_mg,
                                     potassium_mg, cholesterol_mg, carbohydrates_total_g, fiber_g, sugar_g)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        # Data values from the API response
        values = (
            food_item['name'],
            food_item['calories'],
            food_item['serving_size_g'],
            food_item['fat_total_g'],
            food_item['fat_saturated_g'],
            food_item['protein_g'],
            food_item['sodium_mg'],
            food_item['potassium_mg'],
            food_item['cholesterol_mg'],
            food_item['carbohydrates_total_g'],
            food_item['fiber_g'],
            food_item['sugar_g']
        )

        # Execute the SQL query
        cursor.execute(sql, values)

        # Commit the transaction
        conn.commit()

        print(f"Nutrition data for {food_item['name']} has been inserted into the database.")

        # Fetch the total sum of calories from the database
        sum_query = "SELECT SUM(calories) FROM nutrition_info"
        cursor.execute(sum_query)
        total_calories = cursor.fetchone()[0]

        print(f"Total calories in the nutrition_info table: {total_calories}")

        # Close the cursor and connection
        cursor.close()
        conn.close()

    else:
        print("No nutrition information found for the queried item.")
else:
    print(f"Error: {response.status_code}")
