from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

MAKE_WEBHOOK_URL = "https://hook.us1.make.com/YOUR_UNIQUE_WEBHOOK"  # Replace this later

@app.route('/')
def home():
    return '✅ GPT File Upload Bridge Running'

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    response = requests.post(
        MAKE_WEBHOOK_URL,
        files={'file': (file.filename, file.read(), file.content_type)}
    )

    return jsonify({
        "status": "forwarded to Make",
        "make_status": response.status_code,
        "make_response": response.text
    })
