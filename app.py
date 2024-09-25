from flask import Flask, request, jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://sample_user:sample123@cluster0.xig4s.mongodb.net/treasurehunt?retryWrites=true&w=majority"
mongo = PyMongo(app)

@app.route('/add_user', methods=['POST'])
def add_user():
    username = request.form.get('username')
    password = request.form.get('password')
    path_number = request.form.get('path_number')
    round_number = request.form.get('round')
    current_round = request.form.get('current_round')

    user_data = {
        "username": username,
        "password": password,
        "path_number": path_number,
        "round": round_number,
        "current_round": current_round,
    }

    mongo.db.users.insert_one(user_data)
    return jsonify({"message": "User data added successfully."})

@app.route('/add_path_data', methods=['POST'])
def add_path_data():
    path_number = request.form['path_number']
    solution = request.form['solution']
    round_number = request.form['round']
    venue = request.form['venue']
    question = request.form.get('question', '')  # Default to empty string
    image_url = request.form.get('image_url', '')  # Default to empty string
    hint = request.form.get('hint', '')  # Default to empty string

    # Create the collection name based on path_number
    collection_name = f"p{path_number}"
    collection = mongo.db[collection_name]

    # Prepare the data to be inserted
    path_data = {
        "question": question,
        "solution": solution,
        "round": round_number,
        "venue": venue,
        "image_url": image_url,
        "hint": hint,  # Add hint to the collection
    }

    # Insert the data into the collection
    collection.insert_one(path_data)

    return jsonify({"message": "Path data added successfully."})

if __name__ == "__main__":
    app.run(debug=True)
