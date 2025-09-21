from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

cards = []

@app.route("/")
def home():
    return "✅ Card Manager API is running!"

@app.route("/cards", methods=["GET", "POST"])
def manage_cards():
    if request.method == "POST":
        data = request.get_json()
        data["created_at"] = datetime.now().isoformat()
        cards.append(data)
        return jsonify({"message": "Card added successfully", "cards": cards}), 201

    return jsonify(cards)

if __name__ == "__main__":
    app.run(debug=True)
