import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'database', 'nutrisense.db')

def get_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH)

def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()

        # Create Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                age INTEGER,
                gender TEXT,
                height REAL,
                weight REAL,
                activity_level TEXT,
                dietary_preference TEXT,
                health_conditions TEXT,
                allergies TEXT
            )
        ''')

        # Create Recommendations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS recommendations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                date TEXT,
                breakfast TEXT,
                lunch TEXT,
                dinner TEXT,
                snacks TEXT,
                water_intake TEXT,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        ''')

        conn.commit()

def save_user(name, age, gender, height, weight, activity_level, dietary_preference, health_conditions, allergies):
    with get_connection() as conn:
        cursor = conn.cursor()

        # Check if user exists
        cursor.execute("SELECT id FROM users WHERE name=?", (name,))
        row = cursor.fetchone()

        health_str = ",".join(health_conditions) if isinstance(health_conditions, list) else health_conditions
        allergies_str = ",".join(allergies) if isinstance(allergies, list) else allergies

        if row:
            user_id = row[0]
            cursor.execute('''
                UPDATE users
                SET age=?, gender=?, height=?, weight=?, activity_level=?,
                    dietary_preference=?, health_conditions=?, allergies=?
                WHERE id=?
            ''', (age, gender, height, weight, activity_level, dietary_preference, health_str, allergies_str, user_id))
        else:
            cursor.execute('''
                INSERT INTO users (name, age, gender, height, weight, activity_level, dietary_preference, health_conditions, allergies)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (name, age, gender, height, weight, activity_level, dietary_preference, health_str, allergies_str))
            user_id = cursor.lastrowid

        conn.commit()
    return user_id

def get_user(name):
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE name=?", (name,))
        row = cursor.fetchone()
        return dict(row) if row else None
    finally:
        conn.close()

def save_recommendation(user_id, date, breakfast, lunch, dinner, snacks, water_intake):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO recommendations (user_id, date, breakfast, lunch, dinner, snacks, water_intake)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, date, breakfast, lunch, dinner, snacks, water_intake))
        conn.commit()

def get_recommendation_history(user_id):
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM recommendations WHERE user_id=? ORDER BY date DESC", (user_id,))
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()
    
if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")
