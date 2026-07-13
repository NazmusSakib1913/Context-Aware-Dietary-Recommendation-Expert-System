"""
food_data.py
============
Comprehensive food knowledge base with accurate per-serving nutritional values.
Includes Sodium (mg), Fiber (g), and Sugar (g) for precise expert system filtering.

Sources: USDA FoodData Central, BFRI (Bangladesh Food Research Institute).
All values are PER SINGLE SERVING.
"""

import pandas as pd


def get_food_database():
    """Return a DataFrame of all foods with detailed nutritional info."""

    data = [
        # ====================================================================
        # BREAKFAST ITEMS
        # ====================================================================
        # (Name, Category, Calories, Protein, Fat, Carbs, Fiber, Sugar, Sodium_mg,
        #  SuitableFor, AvoidFor, DietType, Allergens, IsBangladeshi)

        # --- Grains / Breads ---
        ("Oats Porridge (1 bowl)", "Breakfast", 154, 5.3, 2.6, 27, 4.0, 1.0, 5,
         "Diabetes,High Cholesterol,High Blood Pressure", "None", "Vegan", "None", False),
        ("Roti / Chapati (2 pcs)", "Breakfast,Lunch,Dinner", 210, 7, 1.5, 43, 4.5, 1.0, 10,
         "Diabetes,High Blood Pressure,High Cholesterol", "None", "Vegan", "None", True),
        ("Paratha (1 pc)", "Breakfast", 260, 5, 13, 33, 1.5, 1.0, 300,
         "None", "Diabetes,High Cholesterol,High Blood Pressure", "Vegan", "None", True),
        ("White Bread Toast (2 slices)", "Breakfast", 160, 5, 2, 30, 1.2, 3.0, 290,
         "None", "Diabetes,High Blood Pressure", "Vegan", "None", False),
        ("Whole Wheat Toast (2 slices)", "Breakfast", 140, 7, 2, 24, 4.0, 2.0, 250,
         "Diabetes,High Cholesterol", "None", "Vegan", "None", False),
        ("Idli (2 pcs)", "Breakfast", 130, 4, 0.5, 28, 1.0, 0.5, 380,
         "Diabetes", "High Blood Pressure", "Vegan", "None", False),
        ("Muri / Puffed Rice (1 cup)", "Breakfast,Snack", 55, 1, 0.2, 12, 0.3, 0.1, 1,
         "High Blood Pressure", "Diabetes", "Vegan", "None", True),
        ("Chira / Flattened Rice (1 cup)", "Breakfast", 110, 2, 0.3, 25, 0.5, 0.5, 3,
         "Anemia", "Diabetes", "Vegan", "None", True),
        ("Peanut Butter Toast (2 slices)", "Breakfast", 320, 12, 17, 28, 3.5, 4.0, 350,
         "Anemia", "High Blood Pressure", "Vegan", "Peanut", False),

        # --- Eggs / Dairy ---
        ("Boiled Egg (2 pcs)", "Breakfast,Snack", 156, 12, 10, 1, 0, 0.5, 125,
         "Anemia,Diabetes", "High Cholesterol", "Non-Vegetarian", "Egg", True),
        ("Egg Omelette (2 eggs)", "Breakfast", 190, 13, 14, 2, 0, 0.5, 320,
         "Anemia", "High Cholesterol,High Blood Pressure", "Non-Vegetarian", "Egg", True),
        ("Milk - Low Fat (1 glass)", "Breakfast,Snack", 100, 8, 2.5, 12, 0, 12, 105,
         "Anemia,High Blood Pressure", "None", "Vegetarian", "Milk", True),
        ("Milk - Full Fat (1 glass)", "Breakfast,Snack", 150, 8, 8, 12, 0, 12, 105,
         "Anemia", "High Cholesterol", "Vegetarian", "Milk", True),
        ("Yogurt - Plain (1 cup)", "Breakfast,Snack", 100, 10, 2, 12, 0, 8, 70,
         "High Blood Pressure,Diabetes", "None", "Vegetarian", "Milk", True),
        ("Lassi - Sweet (1 glass)", "Breakfast,Snack", 170, 6, 3, 28, 0, 22, 80,
         "None", "Diabetes", "Vegetarian", "Milk", True),

        # --- Fruits (Breakfast / Snack) ---
        ("Banana (1 medium)", "Breakfast,Snack", 105, 1.3, 0.4, 27, 3.1, 14, 1,
         "Anemia,High Blood Pressure", "Diabetes,Kidney Disease", "Vegan", "None", True),
        ("Apple (1 medium)", "Breakfast,Snack", 95, 0.5, 0.3, 25, 4.4, 19, 2,
         "Diabetes,High Cholesterol,High Blood Pressure", "None", "Vegan", "None", True),
        ("Guava (1 medium)", "Breakfast,Snack", 68, 2.5, 1, 14, 5.4, 9, 3,
         "Diabetes,High Blood Pressure,High Cholesterol", "None", "Vegan", "None", True),
        ("Papaya (1 cup diced)", "Breakfast,Snack", 55, 0.9, 0.2, 14, 2.5, 8, 4,
         "Diabetes,High Blood Pressure", "Kidney Disease", "Vegan", "None", True),
        ("Watermelon (1 cup)", "Breakfast,Snack", 46, 0.9, 0.2, 11, 0.6, 9, 2,
         "High Blood Pressure", "Diabetes,Kidney Disease", "Vegan", "None", True),

        # ====================================================================
        # LUNCH / DINNER — RICE & GRAINS
        # ====================================================================
        ("White Rice (1 cup cooked)", "Lunch,Dinner", 205, 4.3, 0.4, 45, 0.6, 0.1, 1,
         "Anemia", "Diabetes", "Vegan", "None", True),
        ("Brown Rice (1 cup cooked)", "Lunch,Dinner", 215, 5, 1.8, 45, 3.5, 0.7, 10,
         "Diabetes,High Blood Pressure,High Cholesterol", "None", "Vegan", "None", True),
        ("Khichuri (1 bowl)", "Lunch,Dinner", 230, 8, 5, 38, 3.0, 1.0, 400,
         "Anemia", "High Blood Pressure,Diabetes", "Vegan", "None", True),

        # ====================================================================
        # LUNCH / DINNER — FISH (Non-Vegetarian)
        # ====================================================================
        ("Rui Fish Curry (1 serving)", "Lunch,Dinner", 185, 22, 8, 5, 0.5, 1, 350,
         "Anemia,High Blood Pressure", "None", "Non-Vegetarian", "Seafood", True),
        ("Tilapia Fish Curry (1 serving)", "Lunch,Dinner", 170, 23, 6, 5, 0.5, 1, 320,
         "Diabetes,High Blood Pressure,Anemia", "None", "Non-Vegetarian", "Seafood", True),
        ("Hilsha Fish Curry (1 serving)", "Lunch,Dinner", 310, 22, 22, 5, 0, 1, 60,
         "Anemia", "High Cholesterol,Diabetes", "Non-Vegetarian", "Seafood", True),
        ("Grilled Salmon (1 fillet)", "Lunch,Dinner", 200, 25, 11, 0, 0, 0, 60,
         "High Blood Pressure,High Cholesterol,Diabetes", "None", "Non-Vegetarian", "Seafood", False),
        ("Shrimp / Chingri Curry (1 serving)", "Lunch,Dinner", 180, 18, 8, 8, 0.5, 1, 450,
         "Anemia", "High Cholesterol,High Blood Pressure,Kidney Disease", "Non-Vegetarian", "Seafood", True),
        ("Pabda Fish Curry (1 serving)", "Lunch,Dinner", 160, 20, 7, 4, 0.3, 0.5, 300,
         "Anemia,Diabetes,High Blood Pressure", "None", "Non-Vegetarian", "Seafood", True),

        # ====================================================================
        # LUNCH / DINNER — MEAT (Non-Vegetarian)
        # ====================================================================
        ("Chicken Curry (1 serving)", "Lunch,Dinner", 240, 22, 14, 6, 0.5, 1, 480,
         "Anemia", "High Cholesterol,High Blood Pressure", "Non-Vegetarian", "None", True),
        ("Grilled Chicken Breast (1 pc)", "Lunch,Dinner", 165, 31, 3.6, 0, 0, 0, 75,
         "Diabetes,High Blood Pressure,High Cholesterol,Anemia", "None", "Non-Vegetarian", "None", False),
        ("Chicken Stew (1 bowl)", "Lunch,Dinner", 200, 20, 8, 12, 2, 3, 350,
         "Diabetes,High Blood Pressure,Anemia", "None", "Non-Vegetarian", "None", False),
        ("Beef Curry (1 serving)", "Lunch,Dinner", 300, 24, 20, 6, 0.5, 1, 500,
         "Anemia", "High Blood Pressure,High Cholesterol,Kidney Disease", "Non-Vegetarian", "None", True),
        ("Mutton Curry (1 serving)", "Lunch,Dinner", 290, 22, 18, 5, 0.5, 1, 480,
         "Anemia", "High Blood Pressure,High Cholesterol,Kidney Disease", "Non-Vegetarian", "None", True),
        ("Egg Curry (1 serving)", "Lunch,Dinner", 180, 12, 12, 6, 0.5, 1, 400,
         "Anemia", "High Cholesterol,High Blood Pressure", "Non-Vegetarian", "Egg", True),
        ("Chicken Bhuna (1 serving)", "Lunch,Dinner", 270, 24, 16, 6, 0.5, 1.5, 520,
         "Anemia", "High Cholesterol,High Blood Pressure", "Non-Vegetarian", "None", True),

        # ====================================================================
        # LUNCH / DINNER — DAL / LENTILS (Vegan)
        # ====================================================================
        ("Masoor Dal (1 bowl)", "Lunch,Dinner", 115, 9, 0.4, 20, 4.0, 1, 5,
         "Diabetes,High Blood Pressure,High Cholesterol,Anemia", "Kidney Disease", "Vegan", "None", True),
        ("Mung Dal (1 bowl)", "Lunch,Dinner", 105, 7, 0.4, 18, 3.0, 1, 4,
         "Diabetes,High Blood Pressure,Kidney Disease", "None", "Vegan", "None", True),
        ("Chana Dal (1 bowl)", "Lunch,Dinner", 170, 11, 2, 28, 5.0, 2, 6,
         "Diabetes,High Cholesterol", "Kidney Disease", "Vegan", "None", True),
        ("Mixed Beans Curry (1 bowl)", "Lunch,Dinner", 180, 12, 1.5, 32, 8.0, 2, 350,
         "High Cholesterol,Diabetes", "Kidney Disease,High Blood Pressure", "Vegan", "None", True),

        # ====================================================================
        # LUNCH / DINNER — VEGETABLES (Vegan)
        # ====================================================================
        ("Mixed Vegetables Curry (1 bowl)", "Lunch,Dinner", 90, 3, 3.5, 14, 3.5, 4, 280,
         "Diabetes,High Blood Pressure,High Cholesterol", "None", "Vegan", "None", True),
        ("Spinach / Palong Shak (1 bowl)", "Lunch,Dinner", 40, 3, 0.5, 4, 2.5, 0.5, 65,
         "Anemia,Diabetes,High Blood Pressure,High Cholesterol", "Kidney Disease", "Vegan", "None", True),
        ("Pui Shak (1 bowl)", "Lunch,Dinner", 35, 2.5, 0.3, 4, 2.0, 0.5, 50,
         "Anemia,Diabetes", "Kidney Disease", "Vegan", "None", True),
        ("Lau / Bottle Gourd Curry (1 bowl)", "Lunch,Dinner", 60, 2, 2, 9, 1.5, 3, 40,
         "Diabetes,Kidney Disease,High Blood Pressure", "None", "Vegan", "None", True),
        ("Begun Bharta / Eggplant Mash (1 serving)", "Lunch,Dinner", 80, 2, 4, 10, 3.0, 3, 35,
         "Diabetes,High Blood Pressure,High Cholesterol", "None", "Vegan", "None", True),
        ("Aloo Bhaji / Potato Fry (1 serving)", "Lunch,Dinner", 160, 3, 5, 26, 2.0, 1, 300,
         "Anemia", "Diabetes,High Blood Pressure", "Vegan", "None", True),
        ("Korola Bhaji / Bitter Gourd (1 serving)", "Lunch,Dinner", 50, 2, 1.5, 7, 2.5, 1, 30,
         "Diabetes,High Cholesterol", "None", "Vegan", "None", True),
        ("Broccoli Stir Fry (1 cup)", "Lunch,Dinner", 55, 3, 2, 7, 3.5, 2, 30,
         "Diabetes,High Cholesterol,High Blood Pressure", "None", "Vegan", "None", False),
        ("Cabbage Bhaji (1 serving)", "Lunch,Dinner", 50, 2, 2, 6, 2.5, 3, 25,
         "Diabetes,High Blood Pressure", "None", "Vegan", "None", True),
        ("Shutki Bhorta (1 serving)", "Lunch,Dinner", 120, 18, 4, 2, 0.5, 0, 1200,
         "Anemia", "High Blood Pressure,Kidney Disease", "Non-Vegetarian", "Seafood", True),
        ("Deem Bhorta / Egg Mash (1 serving)", "Lunch,Dinner", 140, 10, 9, 3, 0.5, 0.5, 350,
         "Anemia", "High Cholesterol,High Blood Pressure", "Non-Vegetarian", "Egg", True),
        ("Tofu Curry (1 serving)", "Lunch,Dinner", 140, 10, 8, 6, 1.0, 1, 15,
         "Diabetes,High Cholesterol,High Blood Pressure", "None", "Vegan", "None", False),
        ("Paneer Curry (1 serving)", "Lunch,Dinner", 260, 14, 18, 8, 0.5, 2, 40,
         "Anemia", "High Cholesterol,Diabetes", "Vegetarian", "Milk", False),

        # ====================================================================
        # SNACK ITEMS
        # ====================================================================
        ("Almonds (1 handful / 23 pcs)", "Snack", 160, 6, 14, 6, 3.5, 1, 1,
         "High Cholesterol,Diabetes,High Blood Pressure", "None", "Vegan", "None", False),
        ("Walnuts (7 halves)", "Snack", 95, 2, 9, 2, 1.0, 0.5, 0,
         "High Cholesterol,Diabetes,High Blood Pressure", "None", "Vegan", "None", False),
        ("Orange (1 medium)", "Snack", 62, 1.2, 0.2, 15, 3.0, 12, 1,
         "High Blood Pressure,Anemia,High Cholesterol", "Kidney Disease", "Vegan", "None", True),
        ("Cucumber Salad (1 bowl)", "Snack", 30, 1, 0.2, 6, 1.0, 3, 3,
         "Diabetes,High Blood Pressure,High Cholesterol,Kidney Disease", "None", "Vegan", "None", True),
        ("Chana / Chickpea Snack (1 cup)", "Snack", 130, 7, 2, 22, 6.0, 4, 6,
         "Diabetes,High Cholesterol,Anemia", "Kidney Disease", "Vegan", "None", True),
        ("Dates (3 pcs)", "Snack", 66, 0.5, 0, 18, 1.6, 16, 1,
         "Anemia", "Diabetes", "Vegan", "None", True),
        ("Mixed Fruit Salad (1 bowl)", "Snack", 80, 1, 0.3, 20, 2.5, 14, 3,
         "High Blood Pressure,Anemia,High Cholesterol", "Diabetes", "Vegan", "None", True),
        ("Jhalmuri / Spiced Puffed Rice (1 cup)", "Snack", 150, 3, 4, 26, 1.0, 1, 280,
         "None", "Diabetes,High Blood Pressure", "Vegan", "Peanut", True),
        ("Roasted Makhana / Fox Nuts (1 cup)", "Snack", 100, 4, 0.5, 20, 1.5, 0, 2,
         "Diabetes,High Blood Pressure,High Cholesterol,Kidney Disease", "None", "Vegan", "None", False),
        ("Carrot Sticks (1 cup)", "Snack", 50, 1, 0.3, 12, 3.5, 6, 85,
         "Diabetes,High Blood Pressure,High Cholesterol", "None", "Vegan", "None", True),
        ("Peanuts - Roasted (1 handful)", "Snack", 160, 7, 14, 5, 2.5, 1, 5,
         "Diabetes,High Cholesterol", "None", "Vegan", "Peanut", True),
    ]

    columns = [
        "Food Name", "Category", "Calories", "Protein", "Fat", "Carbs",
        "Fiber", "Sugar", "Sodium",
        "SuitableFor", "AvoidFor", "DietType", "Allergens", "IsBangladeshi"
    ]
    df = pd.DataFrame(data, columns=columns)
    return df
