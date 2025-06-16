import requests
from dotenv import load_dotenv
import os

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("API Key is missing! Please set GEMINI_API_KEY in the .env file.")

# Gemini API URL
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

# Load personal information from the text file
with open("some_information.txt", "r", encoding="utf-8") as file:
    personal_info = file.read()

# Function to check if the user's question is relevant
def is_relevant(question, info):
    question_words = set(question.lower().split())
    info_words = set(info.lower().split())

    # Simple keyword overlap check (can be improved with NLP)
    common_words = question_words.intersection(info_words)
    
    return len(common_words) > 0  # Returns True if there is an overlap

# Chatbot loop
def chat_with_gemini():
    print("Chatbot Ready! (Type 'exit' to quit)\n")

    while True:
        user_query = input("Ask a question: ")
        if user_query.lower() == "exit":
            print("Goodbye!")
            break

        # Check if question is relevant
        if not is_relevant(user_query, personal_info):
            print("\nBot: Sorry, this is not related.\n")
            continue

        # Prepare request for Gemini API
        headers = {"Content-Type": "application/json"}
        data = {
            "contents": [{
                "parts": [{
                    "text": f"Based on the following personal information, answer the question:\n\n{personal_info}\n\nUser Question: {user_query}"
                }]
            }]
        }

        # Send request to Gemini API
        response = requests.post(URL, headers=headers, json=data)

        # Handle response
        if response.status_code == 200:
            response_data = response.json()
            try:
                answer = response_data["candidates"][0]["content"]["parts"][0]["text"]
                print("\nBot:", answer, "\n")
            except KeyError:
                print("\nBot: Sorry, I couldn't generate a response.\n")
        else:
            print("\nBot: Error! Please check your API key or internet connection.\n")

# Run chatbot
chat_with_gemini()
