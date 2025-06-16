from flask import Flask, request, jsonify, render_template
import json
import google.generativeai as genai
from datetime import datetime

# Configure Gemini AI
genai.configure(api_key="AIzaSyDuvblOJw1-8n_rjkzTjKWv_ek2O8C3DTw")

app = Flask(__name__)

# Load data from JSON
def load_data():
    with open("data.json", "r") as file:
        return json.load(file)

# Save query history
def save_data(data):
    with open("data.json", "w") as file:
        json.dump(data, file, indent=4)

# AI-Powered Query Handling
def ai_response(query):
    """Use Gemini AI to generate a response for non-database queries."""
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(query)
    return response.text.strip() if response.text else "I'm not sure how to answer that."

# Extract relevant data from database
def search_database(query):
    """Search for relevant customer data based on user query."""
    database = load_data()
    customers = database["customers"]
    results = []

    query_lower = query.lower()

    for customer in customers:
        if (
            query_lower in customer["name"].lower()
            or query_lower in customer["purchase"].lower()
            or "customer" in query_lower
        ):
            results.append(
                f"👤 **Name:** {customer['name']}<br>"
                f"🛒 **Purchase:** {customer['purchase']}<br>"
                f"📅 **Date:** {customer['date']}<br>"
                "------------------------<br>"
            )

    return "<br>".join(results) if results else None

# Main API Endpoint
@app.route("/api/query", methods=["POST"])
def handle_query():
    data = request.json
    user_query = data.get("query", "").strip()

    # Search database first
    db_result = search_database(user_query)

    if db_result:
        bot_response = db_result  # If found in database, return that
    else:
        bot_response = ai_response(user_query)  # Otherwise, use AI

    # Save query history
    database = load_data()
    new_query = {
        "id": len(database["queries"]) + 1,
        "query": user_query,
        "response": bot_response,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    database["queries"].append(new_query)
    save_data(database)

    return jsonify({"response": bot_response})

# Serve Frontend
@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
