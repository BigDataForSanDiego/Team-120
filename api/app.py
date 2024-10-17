import json
from flask import Flask, jsonify, request
from autopopulate import generate_questions_and_autopopulate

app = Flask(__name__)

profile_data = {}
answers = {}
current_question_index = 0

# run API locally "pyhon -m flask run", assuming you have venv setup with flask installed using pip

# Route to submit the health profile


@app.route('/submit_profile', methods=['POST'])
def submit_profile():
    """Route to submit the health profile and store it."""
    global profile_data

    # Receive the profile from the client
    profile = request.json
    profile_data = profile  # Store the profile data globally

    return jsonify({"message": "Profile submitted successfully"}), 200

# Route to get missing questions


@app.route('/missing_questions', methods=['GET'])
def get_missing_questions():
    """Route to fetch missing questions based on the submitted profile."""
    if not profile_data:
        return jsonify({"error": "No profile data submitted"}), 400

    # Generate missing questions based on the stored profile
    _, missing_questions = generate_questions_and_autopopulate(profile_data)

    return jsonify({"missing_questions": missing_questions}), 200


if __name__ == '__main__':
    app.run(debug=True)
