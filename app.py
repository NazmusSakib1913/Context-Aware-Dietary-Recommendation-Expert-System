"""
app.py
======
Main Streamlit application for NutriSense AI.
Provides multi-page navigation: Home, Profile, Recommendations, Weekly Planner, About.
"""

import streamlit as st
from database import init_db, save_user, get_user, save_recommendation, get_recommendation_history
from expert_system import DietaryExpertSystem
from recommendation import (
    generate_meal_plan, calculate_water_intake,
    calculate_plan_nutrition, generate_weekly_meal_plan, generate_grocery_list
)
from utils import plot_bmi_gauge, plot_macros_pie, plot_calorie_bar, create_pdf_report
import datetime
import pandas as pd

# Initialize the database on startup
init_db()

# ── Page Config ───────────────────────────────────────────────────────
st.set_page_config(
    page_title="NutriSense AI",
    page_icon="🍏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Sidebar Navigation ───────────────────────────────────────────────
st.sidebar.title("🍏 NutriSense AI")
pages = [
    "🏠 Home",
    "👤 Profile & Health Info",
    "📋 Recommendation Dashboard",
    "📅 Weekly Planner & Grocery List",
    "ℹ️ About"
]
choice = st.sidebar.radio("Navigate", pages)

# ======================================================================
# PAGE: HOME
# ======================================================================
if choice == "🏠 Home":
    st.title("Welcome to NutriSense AI 🍏")
    st.subheader("Your Context-Aware Dietary Recommendation Expert System")

    st.markdown("""
    ---
    ### What can NutriSense AI do?

    | Feature | Description |
    |---|---|
    | 🧮 **BMI Calculator** | Automatically calculates and classifies your BMI |
    | 🤖 **Expert System** | Rule-based AI filters unsafe foods and explains every decision |
    | 🍽️ **Meal Plans** | Personalized Breakfast, Lunch, Dinner & Snack recommendations |
    | 📊 **Visualizations** | Interactive charts for BMI, calories, and macronutrients |
    | 📅 **Weekly Planner** | Full 7-day meal plan with a grocery list |
    | 📥 **PDF Export** | Download your meal plan as a PDF report |
    | 🇧🇩 **Bangladeshi Foods** | Option to filter for local Bangladeshi cuisine |

    ---
    👈 **Get started** by navigating to **Profile & Health Info** in the sidebar.
    """)

# ======================================================================
# PAGE: PROFILE & HEALTH INFO
# ======================================================================
elif choice == "👤 Profile & Health Info":
    st.title("👤 User Profile & Health Information")

    with st.form("profile_form"):
        st.subheader("Basic Information")
        col_a, col_b = st.columns(2)
        with col_a:
            name = st.text_input("Full Name", value=st.session_state.get('user_name', ''))
            age = st.number_input("Age", min_value=10, max_value=120, value=25)
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        with col_b:
            height = st.number_input("Height (cm)", min_value=100, max_value=250, value=170)
            weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0, value=70.0)
            activity_level = st.selectbox("Activity Level", ["Low", "Moderate", "High"])

        st.subheader("Health & Dietary Constraints")
        col_c, col_d = st.columns(2)
        with col_c:
            dietary_preference = st.selectbox("Dietary Preference", ["Non-Vegetarian", "Vegetarian", "Vegan"])
            health_conditions = st.multiselect(
                "Health Conditions",
                ["Diabetes", "High Blood Pressure", "High Cholesterol", "Kidney Disease", "Anemia", "None"],
                default=["None"]
            )
        with col_d:
            allergies = st.multiselect(
                "Food Allergies",
                ["Milk", "Peanut", "Egg", "Seafood", "None"],
                default=["None"]
            )

        submitted = st.form_submit_button("💾 Save Profile")

        if submitted:
            if not name.strip():
                st.error("Please enter your name!")
            else:
                save_user(
                    name.strip(), age, gender, height, weight,
                    activity_level, dietary_preference, health_conditions, allergies
                )
                st.session_state['user_name'] = name.strip()
                st.success("✅ Profile saved! Navigate to **Recommendation Dashboard** to see your meal plan.")

# ======================================================================
# PAGE: RECOMMENDATION DASHBOARD
# ======================================================================
elif choice == "📋 Recommendation Dashboard":
    st.title("📋 Your Personalized Dashboard")

    name = st.session_state.get('user_name', '')
    if not name:
        st.warning("⚠️ Please set up your profile first in **Profile & Health Info**.")
    else:
        user_profile = get_user(name)
        if not user_profile:
            st.error("User not found. Please save your profile first.")
        else:
            st.write(f"### Hello, {user_profile['name']}! 👋")

            # Bangladeshi cuisine toggle
            wants_bangladeshi = st.checkbox("🇧🇩 Prefer Bangladeshi Cuisine?", value=True)

            # Initialize Expert System
            expert = DietaryExpertSystem(user_profile)
            bmi_cat = expert.get_bmi_category()
            calorie_target = expert.get_daily_calorie_target()

            # ── Health Summary ────────────────────────────────────────
            st.subheader("Health Summary")
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(plot_bmi_gauge(expert.bmi), use_container_width=True)
            with col2:
                st.metric("BMI Value", expert.bmi)
                st.metric("BMI Category", bmi_cat)
                st.metric("Daily Calorie Target", f"{calorie_target} kcal")
                st.metric("Activity Level", user_profile['activity_level'])
                st.metric("Dietary Preference", user_profile['dietary_preference'])

            # ── Apply Expert System Rules ─────────────────────────────
            filtered_food, explanations, foods_to_avoid = expert.apply_rules(wants_bangladeshi=wants_bangladeshi)

            st.subheader("🤖 Expert System Reasoning")
            for exp in explanations:
                st.info(exp)

            # ── Foods to Avoid ────────────────────────────────────────
            if foods_to_avoid:
                st.subheader("🚫 Foods to Avoid")
                st.warning(", ".join(set(foods_to_avoid)))

            # ── Generate Meal Plan ────────────────────────────────────
            if st.button("🔄 Generate Today's Meal Plan"):
                plan = generate_meal_plan(filtered_food)
                water_intake = calculate_water_intake(user_profile['weight'], user_profile['activity_level'])

                # Save to session state so it persists
                st.session_state['daily_plan'] = plan
                st.session_state['daily_water'] = water_intake

                # Save to database history
                save_recommendation(
                    user_profile['id'],
                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    ", ".join(plan["Breakfast"]),
                    ", ".join(plan["Lunch"]),
                    ", ".join(plan["Dinner"]),
                    ", ".join(plan["Snacks"]),
                    f"{water_intake} Liters"
                )

            # ── Display Plan ──────────────────────────────────────────
            if 'daily_plan' in st.session_state:
                plan = st.session_state['daily_plan']
                water_intake = st.session_state['daily_water']

                st.success("✅ Meal plan generated and saved!")

                st.subheader("🍽️ Recommended Meals")
                m1, m2 = st.columns(2)
                with m1:
                    st.markdown(f"**🌅 Breakfast:** {', '.join(plan['Breakfast']) or 'None'}")
                    st.markdown(f"**🍛 Lunch:** {', '.join(plan['Lunch']) or 'None'}")
                with m2:
                    st.markdown(f"**🌙 Dinner:** {', '.join(plan['Dinner']) or 'None'}")
                    st.markdown(f"**🍎 Snacks:** {', '.join(plan['Snacks']) or 'None'}")
                st.markdown(f"**💧 Daily Water Intake:** {water_intake} Liters")

                # Nutrition charts
                nutrition = calculate_plan_nutrition(plan, filtered_food)
                st.subheader("📊 Nutrition Summary")
                c1, c2 = st.columns(2)
                with c1:
                    st.plotly_chart(plot_calorie_bar(nutrition['Calories'], calorie_target), use_container_width=True)
                with c2:
                    st.plotly_chart(
                        plot_macros_pie(nutrition['Protein'], nutrition['Carbs'], nutrition['Fat']),
                        use_container_width=True
                    )

                # PDF Download
                pdf_path = create_pdf_report(user_profile['name'], plan, f"{water_intake} Liters")
                with open(pdf_path, "rb") as f:
                    st.download_button(
                        label="📥 Download Plan as PDF",
                        data=f.read(),
                        file_name="NutriSense_MealPlan.pdf",
                        mime='application/octet-stream'
                    )

            # ── Recommendation History ────────────────────────────────
            st.subheader("📜 Recommendation History")
            history = get_recommendation_history(user_profile['id'])
            if history:
                df = pd.DataFrame(history).drop(columns=['id', 'user_id'])
                st.dataframe(df, use_container_width=True)
            else:
                st.caption("No history yet. Generate your first meal plan above!")

# ======================================================================
# PAGE: WEEKLY PLANNER & GROCERY LIST
# ======================================================================
elif choice == "📅 Weekly Planner & Grocery List":
    st.title("📅 Weekly Meal Planner")
    name = st.session_state.get('user_name', '')
    if not name:
        st.warning("⚠️ Please set up your profile first in **Profile & Health Info**.")
    else:
        user_profile = get_user(name)
        if user_profile:
            expert = DietaryExpertSystem(user_profile)
            wants_bangladeshi = st.checkbox("🇧🇩 Prefer Bangladeshi Cuisine?", value=True, key="weekly_bd")
            filtered_food, _, _ = expert.apply_rules(wants_bangladeshi=wants_bangladeshi)

            if st.button("🔄 Generate Weekly Plan"):
                weekly_plan = generate_weekly_meal_plan(filtered_food, user_profile['activity_level'])
                st.session_state['weekly_plan'] = weekly_plan
                st.success("✅ Weekly plan generated!")

            if 'weekly_plan' in st.session_state:
                weekly_plan = st.session_state['weekly_plan']

                for day, plan in weekly_plan.items():
                    with st.expander(f"📌 {day}"):
                        st.markdown(f"**🌅 Breakfast:** {', '.join(plan['Breakfast']) or 'None'}")
                        st.markdown(f"**🍛 Lunch:** {', '.join(plan['Lunch']) or 'None'}")
                        st.markdown(f"**🌙 Dinner:** {', '.join(plan['Dinner']) or 'None'}")
                        st.markdown(f"**🍎 Snacks:** {', '.join(plan['Snacks']) or 'None'}")

                st.header("🛒 Grocery List")
                grocery = generate_grocery_list(weekly_plan)

                col1, col2 = st.columns(2)
                items = list(grocery.items())
                half = len(items) // 2
                with col1:
                    for item, qty in items[:half]:
                        st.write(f"✅ {item} — ×{qty}")
                with col2:
                    for item, qty in items[half:]:
                        st.write(f"✅ {item} — ×{qty}")

# ======================================================================
# PAGE: ABOUT
# ======================================================================
elif choice == "ℹ️ About":
    st.title("ℹ️ About NutriSense AI")
    st.markdown("""
    **NutriSense AI** is a university project for the **Artificial Intelligence & Expert System** course.

    ### How it works
    1. The user enters their profile (height, weight, age, health conditions, allergies).
    2. The **Expert System** applies a set of IF-THEN rules to filter out unsafe foods and prioritize suitable ones.
    3. The **Recommendation Engine** randomly samples from the filtered foods to build a daily or weekly meal plan.
    4. Each rule explains *why* it was applied — a core principle of expert systems.

    ### Technology Stack
    | Technology | Purpose |
    |---|---|
    | Python 3 | Core language |
    | Streamlit | Web UI framework |
    | SQLite | Local database |
    | Pandas | Data manipulation |
    | Plotly | Interactive charts |
    | FPDF | PDF report generation |

    ### Project Structure
    ```
    project/
    ├── app.py               # Streamlit UI
    ├── database.py          # SQLite operations
    ├── expert_system.py     # Rule-based expert system
    ├── food_data.py         # Food knowledge base
    ├── recommendation.py    # Meal plan generation
    ├── utils.py             # Charts & PDF utilities
    ├── requirements.txt
    └── README.md
    ```

    ---
    *Built with ❤️ for academic purposes.*
    """)
