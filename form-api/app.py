import json
from flask import Flask, jsonify, request
from flask_cors import CORS
from autopopulate import generate_questions_and_autopopulate

app = Flask(__name__)
CORS(app)

profile_data = {}
autopopulated_questions = {}
missing_questions = []
answers = {}

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


@app.route('/get_profile', methods=['GET'])
def get_profile():
    """Route to return the stored health profile."""
    global profile_data

    # Check if the profile exists
    if not profile_data:
        return jsonify({"error": "No profile data available"}), 404

    # Return the stored health profile
    return jsonify({"profile_data": profile_data}), 200
# Route to get missing questions


@app.route('/missing_questions', methods=['GET'])
def get_missing_questions():
    """Route to fetch missing questions based on the submitted profile."""
    if not profile_data:
        return jsonify({"error": "No profile data submitted"}), 400

    # Generate missing questions based on the stored profile
    _, missing_questions = generate_questions_and_autopopulate(profile_data)

    return jsonify({"missing_questions": missing_questions}), 200


@app.route('/update_question', methods=['POST'])
def update_question():
    """Route to update a specific form question with the user's answer."""
    global form_data

    # Receive the question and answer from the client
    data = request.json
    question = data.get("question")
    answer = data.get("answer")

    if not question or not answer:
        return jsonify({"error": "Missing 'question' or 'answer' field"}), 400

    # Check if the question exists in the form
    if question not in form_data:
        return jsonify({"error": f"The question '{question}' does not exist in the form."}), 400

    # Update the answer for the specific question
    form_data[question] = answer

    return jsonify({"message": f"Updated the form with question '{question}' and answer '{answer}'."}), 200


@app.route('/get_form', methods=['GET'])
def get_form():
    """Route to fetch the entire form (populated and missing questions)."""
    if not profile_data:
        return jsonify({"error": "No profile data submitted"}), 400

    return jsonify({
        "autopopulated_questions": autopopulated_questions,
        "missing_questions": missing_questions
    }), 200


if __name__ == '__main__':
    app.run(debug=True)
