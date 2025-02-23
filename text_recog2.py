import re
import requests
import spacy
import sqlite3

# Load Spacy NLP model
nlp = spacy.load("en_core_web_sm")

# API Details
API_URL = "https://api.calorieninjas.com/v1/nutrition"
API_KEY = "sJA5BDqLJ+VReWp6OtRUKQ==YxdNXHxOjRKreUNH"

# Expanded food list with multi-word items
FOOD_KEYWORDS = {"apple", "banana", "chicken", "rice", "bread", "milk", "egg", "cheese", "tomato", 
                 "potato", "salmon", "broccoli", "carrot", "yogurt", "almond", "pasta", "coffee",
                 "omelet", "sandwich", "pizza", "burger", "cereal", "pancake", "fried rice", 
                 "grilled chicken", "chocolate milk", "chicken tikka", "butter chicken", "dal makhani"}

# Database setup
def setup_database():
    conn = sqlite3.connect("food_tracking.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS FoodLog (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            food TEXT,
            quantity INTEGER,
            calories REAL,
            protein REAL,
            fat REAL,
            carbs REAL
        )
    ''')
    conn.commit()
    conn.close()

def save_to_database(food, quantity, nutrition_data):
    conn = sqlite3.connect("food_tracking.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO FoodLog (food, quantity, calories, protein, fat, carbs) 
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (food, quantity, nutrition_data['calories'], nutrition_data['protein_g'], 
          nutrition_data['fat_total_g'], nutrition_data['carbohydrates_total_g']))
    conn.commit()
    conn.close()

def extract_food_items(text):
    """Extract food items (including multi-word foods) using NLP"""
    doc = nlp(text.lower())
    food_items = {}

    words = [token.text for token in doc]  # Tokenize sentence
    i = 0
    while i < len(words):
        found = False
        for length in range(3, 0, -1):  # Try extracting 3-word, 2-word, then 1-word foods
            phrase = " ".join(words[i:i + length])
            if phrase in FOOD_KEYWORDS:
                food_items[phrase] = 1  # Default quantity is 1 if no number is mentioned
                i += length
                found = True
                break
        if not found:
            i += 1

    return food_items

def get_nutrition(food, quantity):
    """Query CalorieNinjas API for nutrition data"""
    headers = {"X-Api-Key": API_KEY}
    response = requests.get(API_URL, headers=headers, params={"query": f"{quantity} {food}"})
    
    if response.status_code == 200 and response.json()["items"]:
        return response.json()["items"][0]
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

# Setup database
setup_database()

# Get user input
text_input = input("Enter a paragraph containing food items: ")

# Extract food items with quantities
food_dict = extract_food_items(text_input)

if food_dict:
    print("\nExtracted Food Items:", food_dict)
    
    for food, quantity in food_dict.items():
        nutrition_data = get_nutrition(food, quantity)
        if nutrition_data:
            print(f"\nNutrition for {quantity} {food}:")
            print(f"Calories: {nutrition_data['calories']} kcal, Protein: {nutrition_data['protein_g']}g, "
                  f"Fat: {nutrition_data['fat_total_g']}g, Carbs: {nutrition_data['carbohydrates_total_g']}g")

            # Save to database
            save_to_database(food, quantity, nutrition_data)
else:
    print("No food items detected.")
