from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os
import logging

app = Flask(__name__)
CORS(app)

# Initialize OpenAI client with API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ],
            max_tokens=150,
            temperature=0.7
        )

        bot_message = response.choices[0].message.content.strip()
        return jsonify({"reply": bot_message})

    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))