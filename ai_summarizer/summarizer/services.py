import os
import requests

# Load API Key from environment variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Correct Groq API URL for chat completion
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

def summarize_text(input_text):
    """
    Calls the Groq API to generate a response for the given text input.
    """
    if not GROQ_API_KEY:
        return {"error": "Missing API Key. Please check your .env file."}

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mixtral-8x7b-32768",  # Default model (you can change this)
        "messages": [{"role": "user", "content": input_text}],  # User input
        "temperature": 0.7  # Adjust for more/less randomness
    }

    try:
        response = requests.post(GROQ_API_URL, json=data, headers=headers)
        response.raise_for_status()  # Raise an error for failed requests

        # Parse response JSON
        response_json = response.json()
        chat_response = response_json.get("choices", [{}])[0].get("message", {}).get("content", "No response generated.")
        
        return {"response": chat_response}

    except requests.exceptions.RequestException as e:
        return {"error": f"API request failed: {str(e)}"}
