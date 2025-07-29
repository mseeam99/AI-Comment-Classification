# Go to below link and download Ollama from below link (YOU MUST)
#   -   https://ollama.com/download

# Run this command in your terminal
#   -   pip install -r requirements.txt

# START BACKEND using below command. It will run backend in port=5001
#   -   python ollamaCall.py      

from flask import Flask, request, jsonify
from flask_cors import CORS
import ollama

app = Flask(__name__)
CORS(app)

# Pull the Ollama model once at startup
ollama.pull('llama3:8b')

# Function to generate label response
def generateLabelResponseUsingOLLAMA(comment):
    givenPrompt = f"""
    You are an AI assistant trained to classify comments from XFAB, a semiconductor manufacturing company. 
    Based on the comment below, choose **only one** of the following categories and return just the category name (no explanation, no number):

    1. Equipment Failures
    2. Operator Interventions
    3. External Disruptions
    4. Process-Related Issues

    Definitions:
    • Equipment Failures: Mechanical, electrical, or software issues.
    • Operator Interventions: Actions taken to prevent damage or resolve errors.
    • External Disruptions: Power outages, network issues, or environmental factors.
    • Process-Related Issues: Recipe errors, material incompatibility, or configuration problems.

    Comment: "{comment}"
    Label:
    """.strip()

    result = ollama.generate(model='llama3:8b', prompt=givenPrompt)
    return result.get('response', '').strip()

# Function to generate root cause response
def generateRootCauseUsingOLLAMA(comment):
    givenPrompt = f"""
    You are an AI assistant trained to analyze machine comments from XFAB, a semiconductor manufacturing company.
    Based on the comment below, describe the root cause in **no more than 3 words**.

    If the comment is unclear or too vague to determine a root cause, respond with:
    "Root cause unclear"

    Comment: "{comment}"
    Root Cause:
    """.strip()

    result = ollama.generate(model='llama3:8b', prompt=givenPrompt)
    return result.get('response', '').strip()

def map_label_code(code):
    """Map a numeric label (string or int) to its category name."""
    mapping = {
        '1': 'Equipment Failures',
        '2': 'Operator Interventions',
        '3': 'External Disruptions',
        '4': 'Process-Related Issues'
    }
    return mapping.get(str(code).strip(), str(code).strip())

@app.route('/api/get-label', methods=['POST'])
def get_label():
    comment = request.json.get('comment', '')

    # get the raw label code from the model
    raw_code = generateLabelResponseUsingOLLAMA(comment)
    # map numeric code → full category name
    label = map_label_code(raw_code)

    root_cause = generateRootCauseUsingOLLAMA(comment)
    return jsonify({'label': label, 'rootCause': root_cause})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
