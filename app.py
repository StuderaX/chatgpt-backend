from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure OpenAI (environment variable set in Render)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Add a root route to verify deployment
@app.route("/")
def home():
    return "ChatGPT backend is running! Use /chat for requests."

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message")

    if not user_message:
        return jsonify({"error": "No message provided."}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ],
            max_tokens=150,
            temperature=0.7
        )

        bot_message = response.choices[0].message['content'].strip()
        return jsonify({"reply": bot_message})  # Changed key to "reply" to match your frontend

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Required for Render deployment
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))