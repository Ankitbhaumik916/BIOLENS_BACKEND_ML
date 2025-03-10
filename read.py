import requests

# Your USDA FoodData Central API key
api_key = "ZT5P9x9vXDlq7k5hVXPYyfLzxVGxpOBShdAZaxon"

# Function to search for food items based on a query
def search_food(query):
    search_url = "https://api.nal.usda.gov/fdc/v1/foods/search"
    
    # Parameters for the search request
    search_params = {
        "query": query,  # User search query (e.g., "apple", "rice", etc.)
        "api_key": api_key,
        "pageSize": 10,  # Limit the results for easier output
    }

    # Make the search request
    response = requests.get(search_url, params=search_params)

    # If the response is successful, return the list of food items
    if response.status_code == 200:
        search_results = response.json()
        return search_results.get('foods', [])
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return []

# Function to filter food items based on target calories
def get_food_by_calories(target_calories):
    # For simplicity, we use a list of common meal items to search for
    meal_items = ["apple", "banana", "rice", "bread", "pasta", "chicken", "broccoli", "carrot", "milk", "egg"]
    
    suggested_meals = []
    
    for item in meal_items:
        # Search food items using the USDA API
        foods = search_food(item)
        
        for food in foods:
            # Find food items that are close to the target calorie range
            for nutrient in food['foodNutrients']:
                if nutrient['nutrientName'] == "Energy" and nutrient['unitName'] == "kcal":
                    if abs(nutrient['value'] - target_calories) <= 50:  # Tolerance of 50 calories
                        suggested_meals.append({
                            "name": food['description'],
                            "calories": nutrient['value'],
                            "fdcId": food['fdcId']
                        })
                    break
    
    return suggested_meals

# Main function to run the program
def main():
    # Take target calorie input from the user
    target_calories = float(input("Enter target calories for the meal: "))

    # Get meal suggestions based on the target calories
    meal_suggestions = get_food_by_calories(target_calories)

    # Output the suggested meals
    if meal_suggestions:
        print(f"Meals close to {target_calories} calories:")
        for meal in meal_suggestions:
            print(f" - {meal['name']}: {meal['calories']} kcal (FDC ID: {meal['fdcId']})")
    else:
        print(f"No meal suggestions found for {target_calories} calories.")

# Run the main function
if __name__ == "__main__":
    main()
