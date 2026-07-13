"""
recommendation.py
==================
Generates meal plans and grocery lists from the filtered food DataFrame.
Uses the expert system's output to build Breakfast / Lunch / Dinner / Snack plans.
"""

import random


def generate_meal_plan(filtered_df):
    """Pick foods for each meal slot from the filtered DataFrame."""
    plan = {
        "Breakfast": [],
        "Lunch": [],
        "Dinner": [],
        "Snacks": []
    }

    if filtered_df.empty:
        return plan

    # Separate foods by meal category
    breakfast_foods = filtered_df[filtered_df['Category'].str.contains('Breakfast', case=False, na=False)]['Food Name'].tolist()
    lunch_foods = filtered_df[filtered_df['Category'].str.contains('Lunch', case=False, na=False)]['Food Name'].tolist()
    dinner_foods = filtered_df[filtered_df['Category'].str.contains('Dinner', case=False, na=False)]['Food Name'].tolist()
    snack_foods = filtered_df[filtered_df['Category'].str.contains('Snack', case=False, na=False)]['Food Name'].tolist()

    # Pick items (3 breakfast, 3 lunch, 3 dinner, 2 snacks)
    if breakfast_foods:
        plan["Breakfast"] = random.sample(breakfast_foods, min(3, len(breakfast_foods)))
    if lunch_foods:
        plan["Lunch"] = random.sample(lunch_foods, min(3, len(lunch_foods)))
    if dinner_foods:
        plan["Dinner"] = random.sample(dinner_foods, min(3, len(dinner_foods)))
    if snack_foods:
        plan["Snacks"] = random.sample(snack_foods, min(2, len(snack_foods)))

    return plan


def calculate_water_intake(weight, activity_level):
    """Estimate daily water intake in Liters."""
    try:
        weight_kg = float(weight)
        water_ml = weight_kg * 35  # Base: 35 ml per kg
        if activity_level == "Moderate":
            water_ml += 500
        elif activity_level == "High":
            water_ml += 1000
        return round(water_ml / 1000.0, 1)
    except (ValueError, TypeError):
        return 2.5


def calculate_plan_nutrition(plan, food_df):
    """Sum up macros for all foods in the given meal plan."""
    all_foods = []
    for meal, foods in plan.items():
        all_foods.extend(foods)

    selected = food_df[food_df['Food Name'].isin(all_foods)]

    return {
        "Calories": round(selected['Calories'].sum(), 1),
        "Protein": round(selected['Protein'].sum(), 1),
        "Fat": round(selected['Fat'].sum(), 1),
        "Carbs": round(selected['Carbs'].sum(), 1)
    }


def generate_weekly_meal_plan(filtered_df, activity_level):
    """Generate a unique meal plan for each day of the week."""
    days = ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    weekly_plan = {}
    for day in days:
        weekly_plan[day] = generate_meal_plan(filtered_df)
    return weekly_plan


def generate_grocery_list(weekly_plan):
    """Aggregate all food items across the week into a grocery list with counts."""
    grocery = {}
    for day, plan in weekly_plan.items():
        for meal, foods in plan.items():
            for food in foods:
                grocery[food] = grocery.get(food, 0) + 1
    # Sort by count descending
    return dict(sorted(grocery.items(), key=lambda x: x[1], reverse=True))
