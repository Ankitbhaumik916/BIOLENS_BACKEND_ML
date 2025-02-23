import re
import requests

# API Details
API_URL = "https://api.calorieninjas.com/v1/nutrition"
API_KEY = "sJA5BDqLJ+VReWp6OtRUKQ==YxdNXHxOjRKreUNH"

# Sample list of food items (extendable)
FOOD_KEYWORDS = {"apple","apples" ,"banana", "chicken", "rice", "bread", "milk", "egg", "cheese", "tomato", 
                 "potato", "salmon", "broccoli", "carrot", "yogurt", "almond", "pasta", "coffee",
                 "omelet", "sandwich", "pizza", "burger", "cereal", "pancake"}

def extract_food_items(text):
    """Extract food items along with quantities from the input text"""
    matches = re.findall(r'(\d+)\s*([a-zA-Z]+)', text.lower())  # Extract quantity + food
    food_items = {}

    for qty, item in matches:
        if item in FOOD_KEYWORDS:  # Check if it's a valid food
            food_items[item] = int(qty)  # Store food with quantity

    return food_items

def get_nutrition(food, quantity):
    """Query CalorieNinjas API for nutrition data"""
    headers = {"X-Api-Key": API_KEY}
    response = requests.get(API_URL, headers=headers, params={"query": f"{quantity} {food}"})
    
    if response.status_code == 200:
        return response.json()["items"]
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

# Get user input
text_input = input("Enter a paragraph containing food items: ")

# Extract food items with quantities
food_dict = extract_food_items(text_input)

if food_dict:
    print("\nExtracted Food Items with Quantities:", food_dict)
    
    for food, quantity in food_dict.items():
        nutrition_data = get_nutrition(food, quantity)
        if nutrition_data:
            print(f"\nNutrition for {quantity} {food}:")
            for item in nutrition_data:
                print(f"Calories: {item['calories']} kcal, Protein: {item['protein_g']}g, "
                      f"Fat: {item['fat_total_g']}g, Carbs: {item['carbohydrates_total_g']}g")
else:
    print("No food items detected.")
