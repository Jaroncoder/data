from flask import Flask, request, jsonify, g
from pymongo import MongoClient
import os

app = Flask(__name__)

# Make sure to set this environment variable in Vercel or in a .env file for local use
# Example: os.getenv("MONGO_URI")
MONGO_URI = os.getenv("MONGO_URI") or "mongodb+srv://sample_user:sample123@cluster0.xig4s.mongodb.net/treasurehunt?retryWrites=true&w=majority"

# Function to get MongoDB client and database
def get_db():
    if not hasattr(g, 'mongo_client'):
        g.mongo_client = MongoClient(MONGO_URI)
    return g.mongo_client.treasurehunt  # Replace 'treasurehunt' with your database name

# Close MongoDB connection after each request
@app.teardown_appcontext
def close_connection(exception):
    if hasattr(g, 'mongo_client'):
        g.mongo_client.close()

# Route to add a new user
@app.route('/add_user', methods=['POST'])
def add_user():
    db = get_db()  # Get the MongoDB database
    users_collection = db.users  # Access the 'users' collection

    # Extract form data from the request
    username = request.form.get('username')
    password = request.form.get('password')
    path_number = request.form.get('path_number')
    round_number = request.form.get('round')
    current_round = request.form.get('current_round')

    # User data
    user_data = {
        "username": username,
        "password": password,
        "path_number": path_number,
        "round": round_number,
        "current_round": current_round,
    }

    # Insert user data into the collection
    users_collection.insert_one(user_data)

    return jsonify({"message": "User data added successfully."})

# Route to add path data for specific path_number
@app.route('/add_path_data', methods=['POST'])
def add_path_data():
    db = get_db()  # Get the MongoDB database

    # Extract form data from the request
    path_number = request.form.get('path_number')
    question = request.form.get('question', '')  # Optional question
    solution = request.form.get('solution')
    round_number = request.form.get('round')
    venue = request.form.get('venue')
    image_url = request.form.get('image_url', '')  # Optional image URL

    # Dynamically access collection based on path_number (e.g., p1, p2)
    collection_name = f"p{path_number}"
    collection = db[collection_name]

    # Prepare the path data
    path_data = {
        "question": question,
        "solution": solution,
        "round": round_number,
        "venue": venue,
        "image_url": image_url
    }

    # Insert the data into the collection
    collection.insert_one(path_data)

    return jsonify({"message": f"Path data added to collection '{collection_name}' successfully."})

# Route to fetch a user's question from their path collection
@app.route('/fetch_question', methods=['POST'])
def fetch_question():
    db = get_db()  # Get the MongoDB database

    username = request.form.get('username')
    round_number = request.form.get('round')

    # Fetch user data to get the path_number
    users_collection = db.users
    user = users_collection.find_one({"username": username})

    if not user:
        return jsonify({"error": "User not found."}), 404

    path_number = user.get('path_number')

    # Access the correct collection based on path_number
    collection_name = f"p{path_number}"
    collection = db[collection_name]

    # Fetch question data based on round
    question_data = collection.find_one({"round": round_number})

    if not question_data:
        return jsonify({"error": "Question not found for this round."}), 404

    return jsonify({
        "question": question_data.get('question'),
        "image_url": question_data.get('image_url', None)  # Provide image URL if available
    })

if __name__ == "__main__":
    app.run(debug=True)
