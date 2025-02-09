from flask import Flask
from flask_socketio import SocketIO, emit
import time
from transformers import pipeline
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for REST API

# Explicitly allow WebSocket connections from React frontend
socketio = SocketIO(app, cors_allowed_origins="http://localhost:3000")

# Load GPT-2 model for text generation
generator = pipeline("text-generation", model="gpt2")


@socketio.on("user_message")
def handle_user_message(data):
    """Handles incoming user messages and generates a response using GPT-2."""
    user_message = data["message"]
    
    # Notify frontend that the bot is typing
    emit("bot_typing", {}, broadcast=True)

    time.sleep(2)  # Simulate typing delay

    # Generate text response using GPT-2
    response = generator(user_message, max_length=10, do_sample=True,truncation = True)
    bot_response = response[0]["generated_text"]

    # Send bot response back to frontend
    emit("bot_response", {"message": bot_response}, broadcast=True)


if __name__ == "__main__":
    # Run the WebSocket server
    socketio.run(app, debug=True, host="127.0.0.1", port=5000)

