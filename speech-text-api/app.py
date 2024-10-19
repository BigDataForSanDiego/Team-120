import json
from flask import Flask, jsonify, request
from autopopulate import generate_questions_and_autopopulate

app = Flask(__name__)

# run API locally "pyhon -m flask run", assuming you have venv setup with flask installed using pip

# Route to submit the health profile


@app.route('/submit_speech', methods=['POST'])
def submit_profile():
    return


@app.route('/get_text', methods=['GET'])
def submit_profile():
    return


if __name__ == '__main__':
    app.run(debug=True)
