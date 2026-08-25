import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS so Google Sites can talk to your backend

@app.route("/")
def home():
    return "Chatbot Backend is running!"

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "").strip().lower()
    
    if not user_message:
        bot_response = "Please type a message!"
    elif "hello" in user_message or "hi" in user_message:
        bot_response = "Hello from my cloud-hosted chatbot! How can I help?"
    else:
        bot_response = f"I received your message: '{user_message}'"

    return jsonify({"response": bot_response})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)