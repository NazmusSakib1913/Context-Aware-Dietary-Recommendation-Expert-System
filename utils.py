# pyrefly: ignore [missing-import]
"""
utils.py
========
Visualization helpers (Plotly) and PDF report generation (FPDF).
"""

import plotly.express as px
import plotly.graph_objects as go
from fpdf import FPDF
import os
import tempfile


def plot_bmi_gauge(bmi):
    """Create a gauge chart showing BMI value with color-coded ranges."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=bmi,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Body Mass Index (BMI)"},
        gauge={
            'axis': {'range': [10, 45]},
            'steps': [
                {'range': [10, 18.5], 'color': "#74b9ff"},   # Underweight
                {'range': [18.5, 25], 'color': "#00b894"},    # Normal
                {'range': [25, 30], 'color': "#fdcb6e"},      # Overweight
                {'range': [30, 45], 'color': "#e17055"}       # Obese
            ],
            'bar': {'color': "#2d3436"},
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': bmi
            }
        }
    ))
    fig.update_layout(height=300)
    return fig


def plot_macros_pie(protein, carbs, fat):
    """Create a donut chart of macronutrient distribution."""
    labels = ['Protein', 'Carbs', 'Fat']
    values = [protein, carbs, fat]
    colors = ['#0984e3', '#00b894', '#e17055']

    fig = px.pie(
        values=values, names=labels,
        title='Macronutrient Distribution',
        hole=0.4,
        color_discrete_sequence=colors
    )
    fig.update_traces(textinfo='label+percent+value', texttemplate='%{label}<br>%{value:.1f}g (%{percent})')
    fig.update_layout(height=350)
    return fig


def plot_calorie_bar(calories, target=2000):
    """Bar chart comparing plan calories against the user's daily target."""
    fig = go.Figure([
        go.Bar(
            x=['Your Plan', f'Target ({int(target)})'],
            y=[calories, target],
            marker_color=['#0984e3', '#b2bec3']
        )
    ])
    fig.update_layout(
        title_text='Daily Calories Comparison',
        yaxis_title='Calories (kcal)',
        height=350
    )
    return fig


def create_pdf_report(name, plan, water):
    """Generate a simple PDF meal plan report. Returns a path to a temp file.

    Uses NamedTemporaryFile (mktemp is insecure / deprecated) and registers
    an atexit hook so the file is cleaned up on interpreter exit.
    """
    import atexit

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 12, "NutriSense AI - Meal Plan Report", ln=True, align='C')

    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"Prepared for: {name}", ln=True, align='C')
    pdf.cell(0, 8, f"Date: {__import__('datetime').datetime.now().strftime('%Y-%m-%d')}", ln=True, align='C')
    pdf.ln(10)

    pdf.set_font("Arial", 'B', 13)
    pdf.cell(0, 10, "Today's Meal Plan", ln=True)
    pdf.set_font("Arial", size=11)

    meals = [
        ("Breakfast", plan.get('Breakfast', [])),
        ("Lunch", plan.get('Lunch', [])),
        ("Dinner", plan.get('Dinner', [])),
        ("Snacks", plan.get('Snacks', []))
    ]
    for meal_name, items in meals:
        pdf.cell(0, 8, f"  {meal_name}: {', '.join(items) if items else 'None'}", ln=True)

    pdf.ln(5)
    pdf.cell(0, 8, f"  Daily Water Intake: {water}", ln=True)

    # NamedTemporaryFile gives a unique path atomically (mktemp is insecure).
    fd, temp_path = tempfile.mkstemp(suffix=".pdf")
    os.close(fd)
    pdf.output(temp_path)
    atexit.register(lambda p=temp_path: os.path.exists(p) and os.remove(p))
    return temp_path
