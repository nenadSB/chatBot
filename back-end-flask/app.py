from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv
import os
import logging

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
# Enable CORS for specific origins (e.g., your Angular frontend at http://localhost:4200)
CORS(app, resources={r"/*": {"origins": "http://localhost:4200"}})

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Validate OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY is not set in the .env file.")

# Debug: Print the OpenAI API key to confirm it's loaded correctly
logging.debug(f"OpenAI API Key: {openai_api_key}")  # Use logging instead of print for consistency

# Initialize the OpenAI client
client = OpenAI(api_key=openai_api_key)

# Define the chatbot route
@app.route("/chat", methods=["POST"])
def chat():
    try:
        # Get user input from the request
        user_input = request.json.get("message")
        if not user_input:
            return jsonify({"error": "Message is required."}), 400

        # Log the received message
        app.logger.debug(f"Received message: {user_input}")

        # Call OpenAI API to generate a response
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Use GPT-3.5
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input},
            ],
        )

        # Log the OpenAI API response
        app.logger.debug(f"OpenAI API response: {response}")

        # Extract the chatbot's response
        chatbot_response = response.choices[0].message.content

        # Log the chatbot's response
        app.logger.debug(f"Chatbot response: {chatbot_response}")

        # Return the response as JSON
        return jsonify({"response": chatbot_response})

    except Exception as e:
        # Log any errors that occur
        app.logger.error(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
