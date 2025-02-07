from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Set your OpenAI API key from the environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise ValueError("The OPENAI_API_KEY environment variable is not set.")

# A simple root route to verify the app is running
@app.route("/")
def home():
    return "ChatGPT backend is running! Use /chat for requests."

# Chat route that uses the new ChatCompletion API
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message")
    
    if not user_message:
        return jsonify({"error": "No message provided."}), 400

    try:
        # Call the new ChatCompletion endpoint
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # The chat model to use
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ],
            max_tokens=150,
            temperature=0.7
        )

        # Extract the bot's reply from the response
        bot_message = response["choices"][0]["message"]["content"].strip()
        return jsonify({"reply": bot_message})

    except Exception as e:
        # Return any error encountered as JSON
        return jsonify({"error": str(e)}), 500

# For deployment (Render will use this entry point)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
