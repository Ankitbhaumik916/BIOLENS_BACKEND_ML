import re
import requests
import spacy
import sqlite3

# Load NLP model
nlp = spacy.load("en_core_web_sm")

# API Details
API_URL = "https://api.calorieninjas.com/v1/nutrition"
API_KEY = "sJA5BDqLJ+VReWp6OtRUKQ==YxdNXHxOjRKreUNH"

# Unit conversion for standardization
UNIT_CONVERSIONS = {
    "kg": 1000, "g": 1, "grams": 1, "kilograms": 1000,
    "ml": 1, "l": 1000, "liters": 1000, "milliliters": 1
}

NEGATION_WORDS = {"no", "not", "never", "didn't", "don't", "did not", "do not"}

def setup_database():
    conn = sqlite3.connect("food_tracking.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS FoodLog (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            food TEXT,
            quantity REAL,
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

def get_nutrition(food, quantity):
    """Query API for valid food names & nutrition data"""
    headers = {"X-Api-Key": API_KEY}
    response = requests.get(API_URL, headers=headers, params={"query": food})

    if response.status_code == 200 and response.json()["items"]:
        return response.json()["items"][0]
    else:
        return None

def extract_food_items(text):
    """Extract words from text, check API, and fetch quantities"""
    doc = nlp(text.lower())
    tokens = [token.text for token in doc]

    possible_foods = {token.text for token in doc if token.pos_ in {"NOUN", "PROPN"}}

    # Identify negated words
    negated_foods = set()
    for i, token in enumerate(tokens):
        if token in possible_foods and i > 0:
            prev_word = tokens[i - 1]
            prev_bigram = " ".join(tokens[i - 2:i]) if i >= 2 else ""
            
            if prev_word in NEGATION_WORDS or prev_bigram in NEGATION_WORDS:
                negated_foods.add(token)

    # Filter out negated foods
    valid_foods = {}
    for word in possible_foods - negated_foods:
        nutrition_data = get_nutrition(word, 100)
        if nutrition_data:
            valid_foods[word] = 1  # Default quantity 1

    # Detect quantities
    for i, token in enumerate(tokens):
        if token in valid_foods:
            quantity = 1
            if i > 0:
                match = re.match(r"(\d+(\.\d+)?)\s*(kg|g|grams|kilograms|ml|l|liters|milliliters)?", tokens[i - 1])
                if match:
                    num = float(match.group(1))
                    unit = match.group(3)
                    if unit and unit in UNIT_CONVERSIONS:
                        num *= UNIT_CONVERSIONS[unit]
                    quantity = num
            valid_foods[token] = quantity

    return valid_foods

# Setup database
setup_database()

# Get user input
text_input = input("Enter a paragraph containing food items: ")

# Extract food items dynamically
food_dict = extract_food_items(text_input)

if food_dict:
    print("\nExtracted Food Items:", food_dict)
    
    for food, quantity in food_dict.items():
        nutrition_data = get_nutrition(food, quantity)
        if nutrition_data:
            print(f"\nNutrition for {quantity}g of {food}:")
            print(f"Calories: {nutrition_data['calories']} kcal, Protein: {nutrition_data['protein_g']}g, "
                  f"Fat: {nutrition_data['fat_total_g']}g, Carbs: {nutrition_data['carbohydrates_total_g']}g")

            # Save to database
            save_to_database(food, quantity, nutrition_data)
else:
    print("No valid food items detected.")
