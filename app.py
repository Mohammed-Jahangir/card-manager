# Step 1: Imports & DB setup
import sqlite3
from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

# Initialize database & table
def init_db():
    conn = sqlite3.connect("cards.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bank TEXT,
            name TEXT,
            type TEXT,
            "limit" REAL,
            interest_rate REAL,
            due_date TEXT,
            rewards TEXT,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()  # run this once at startup

# Step 2: Routes
@app.route("/")
def home():
    return "✅ Card Manager API is running!"

@app.route("/cards", methods=["GET", "POST"])
def manage_cards():
    conn = sqlite3.connect("cards.db")
    cursor = conn.cursor()

    if request.method == "POST":
        data = request.get_json()

        required_fields = ["bank", "name", "type", "limit", "interest_rate", "due_date", "rewards"]
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            conn.close()
            return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

        created_at = datetime.now().isoformat()

        cursor.execute("""
            INSERT INTO cards (bank, name, type, "limit", interest_rate, due_date, rewards, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data["bank"], data["name"], data["type"], data["limit"],
            data["interest_rate"], data["due_date"], data["rewards"], created_at
        ))
        conn.commit()
        conn.close()
        return jsonify({"message": "Card added successfully"}), 201

    cursor.execute("SELECT * FROM cards")
    rows = cursor.fetchall()
    conn.close()

    cards_list = []
    for row in rows:
        card = {
            "id": row[0],
            "bank": row[1],
            "name": row[2],
            "type": row[3],
            "limit": row[4],
            "interest_rate": row[5],
            "due_date": row[6],
            "rewards": row[7],
            "created_at": row[8]
        }
        cards_list.append(card)

    return jsonify(cards_list)

# Step 3: Run server
if __name__ == "__main__":
    app.run(debug=True)
