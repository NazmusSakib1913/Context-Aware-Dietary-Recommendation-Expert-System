"""
expert_system.py
================
Rule-based expert system that filters and prioritizes food
recommendations based on user profile, health conditions,
allergies, BMI, and dietary preferences.

Each rule explains WHY it was applied so the user understands
the reasoning (a core feature of expert systems).
"""

import pandas as pd
from food_data import get_food_database


class DietaryExpertSystem:
    """Core expert system class that applies dietary rules."""

    def __init__(self, user_profile):
        self.user = user_profile
        self.food_df = get_food_database()
        self.bmi = self.calculate_bmi()

    # ------------------------------------------------------------------
    # BMI Calculation
    # ------------------------------------------------------------------
    def calculate_bmi(self):
        """Calculate Body Mass Index from height (cm) and weight (kg)."""
        try:
            height_m = float(self.user['height']) / 100.0
            weight = float(self.user['weight'])
            if height_m > 0:
                return round(weight / (height_m ** 2), 2)
        except (ValueError, TypeError, ZeroDivisionError):
            pass
        return 0.0

    def get_bmi_category(self):
        """Classify BMI into a human-readable category."""
        if self.bmi == 0:
            return "Unknown"
        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi < 25:
            return "Normal"
        elif self.bmi < 30:
            return "Overweight"
        else:
            return "Obese"

    # ------------------------------------------------------------------
    # Daily calorie target based on activity level and BMI
    # ------------------------------------------------------------------
    def get_daily_calorie_target(self):
        """Estimate daily calorie needs based on BMI category and activity."""
        activity = self.user.get('activity_level', 'Moderate')

        bmi_cat = self.get_bmi_category()
        # Base targets
        if bmi_cat == "Underweight":
            base = 2200
        elif bmi_cat == "Normal":
            base = 2000
        elif bmi_cat == "Overweight":
            base = 1600
        else:  # Obese
            base = 1400

        # Adjust for activity
        if activity == "Low":
            base -= 200
        elif activity == "High":
            base += 300

        return base

    # ------------------------------------------------------------------
    # Rule Engine
    # ------------------------------------------------------------------
    def apply_rules(self, wants_bangladeshi=False):
        """
        Apply all expert system rules sequentially and return
        (filtered_dataframe, list_of_explanations).
        """
        filtered_df = self.food_df.copy()
        explanations = []
        foods_to_avoid = []

        # ── Rule 1: Dietary Preference ────────────────────────────────
        pref = self.user.get('dietary_preference', 'Non-Vegetarian')
        if pref == "Vegetarian":
            filtered_df = filtered_df[filtered_df['DietType'].isin(['Vegetarian', 'Vegan'])]
            explanations.append(
                "🥬 Meat and fish removed because your dietary preference is **Vegetarian**."
            )
        elif pref == "Vegan":
            filtered_df = filtered_df[filtered_df['DietType'] == 'Vegan']
            explanations.append(
                "🌱 All animal products removed because your dietary preference is **Vegan**."
            )
        # Non-Vegetarian keeps everything — no filter needed.

        # ── Rule 2: Allergy Filtering ─────────────────────────────────
        allergies_raw = self.user.get('allergies', '')
        if allergies_raw and allergies_raw != "None":
            allergy_list = [a.strip() for a in allergies_raw.split(',') if a.strip() and a.strip() != "None"]
            for allergy in allergy_list:
                before_count = len(filtered_df)
                filtered_df = filtered_df[~filtered_df['Allergens'].str.contains(allergy, case=False, na=False)]
                removed = before_count - len(filtered_df)
                if removed > 0:
                    explanations.append(
                        f"⚠️ Removed {removed} food(s) containing **{allergy}** due to your allergy."
                    )

        # ── Rule 3: Health Conditions — Avoid unsafe foods ────────────
        conditions_raw = self.user.get('health_conditions', '')
        if conditions_raw and conditions_raw != "None":
            condition_list = [c.strip() for c in conditions_raw.split(',') if c.strip() and c.strip() != "None"]
            for cond in condition_list:
                # Find foods to avoid for this condition
                avoid_mask = filtered_df['AvoidFor'].apply(
                    lambda x: cond in [item.strip() for item in str(x).split(',')] if x != "None" else False
                )
                avoided_foods = filtered_df[avoid_mask]['Food Name'].tolist()
                if avoided_foods:
                    foods_to_avoid.extend(avoided_foods)
                    filtered_df = filtered_df[~avoid_mask]
                    explanations.append(
                        f"🚫 Avoided **{', '.join(avoided_foods)}** because they are restricted for **{cond}**."
                    )

        # ── Rule 4: Health Conditions — Prioritize suitable foods ─────
        if conditions_raw and conditions_raw != "None":
            condition_list = [c.strip() for c in conditions_raw.split(',') if c.strip() and c.strip() != "None"]
            # Sum a priority score across ALL conditions: a food suitable for more of
            # your conditions ranks higher. (Previously each iteration overwrote the
            # score, so only the last condition had any effect on ordering.)
            filtered_df['_priority'] = filtered_df['SuitableFor'].apply(
                lambda x: sum(
                    1 for cond in condition_list
                    if cond in [item.strip() for item in str(x).split(',')]
                )
            )
            # Sort so suitable foods come first (used by recommendation engine)
            filtered_df = filtered_df.sort_values('_priority', ascending=False)
            filtered_df = filtered_df.drop(columns=['_priority'])
            explanations.append(
                "✅ Prioritized foods that are specifically recommended for your health condition(s)."
            )

        # ── Rule 5: BMI-based calorie guidance ────────────────────────
        bmi_cat = self.get_bmi_category()
        calorie_target = self.get_daily_calorie_target()

        if bmi_cat == "Obese":
            # Remove very high calorie items (> 280 per serving)
            filtered_df = filtered_df[filtered_df['Calories'] <= 280]
            explanations.append(
                f"🔻 Removed high-calorie foods (>280 kcal/serving) because your BMI is **{self.bmi}** ({bmi_cat}). "
                f"Daily target: ~{calorie_target} kcal."
            )
        elif bmi_cat == "Overweight":
            # Remove very high calorie items (> 300 per serving)
            filtered_df = filtered_df[filtered_df['Calories'] <= 300]
            explanations.append(
                f"📉 Removed high-calorie foods (>300 kcal/serving) because your BMI is **{self.bmi}** ({bmi_cat}). "
                f"Daily target: ~{calorie_target} kcal."
            )
        elif bmi_cat == "Underweight":
            explanations.append(
                f"📈 Including calorie-dense foods because your BMI is **{self.bmi}** ({bmi_cat}). "
                f"Daily target: ~{calorie_target} kcal."
            )
        else:
            explanations.append(
                f"✅ Your BMI is **{self.bmi}** ({bmi_cat}). Daily target: ~{calorie_target} kcal."
            )

        # ── Rule 6: Bangladeshi Food Preference (Bonus) ──────────────
        if wants_bangladeshi:
            bd_filtered = filtered_df[filtered_df['IsBangladeshi'] == True]
            if len(bd_filtered) >= 8:
                filtered_df = bd_filtered
                explanations.append(
                    "🇧🇩 Filtered to show Bangladeshi cuisine options."
                )
            else:
                explanations.append(
                    "🇧🇩 Not enough Bangladeshi foods after filtering — showing all available foods."
                )

        return filtered_df, explanations, foods_to_avoid
