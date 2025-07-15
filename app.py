from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# ✅ Replace this with your real Make.com webhook URL
MAKE_WEBHOOK_URL = os.getenv("MAKE_WEBHOOK_URL", "https://hook.eu2.make.com/4bwkcdcowvn7xs96cg6jgglnt4m2l2yd")

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

# ✅ REQUIRED: This makes it work on Render’s free port system
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

