import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("❌ Gemini API Key not found. Check your .env file.")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Initialize the model
model = genai.GenerativeModel("models/gemini-2.5-flash")

def get_home_remedies(disease_name: str):
    """
    Given a disease name, this function asks Gemini API to suggest
    3-5 simple home remedies.
    """
    prompt = f"""
    You are a friendly health assistant.
    Suggest 3-5 simple home remedies that a person can try at home for the disease: {disease_name}.
    Keep the instructions clear and easy to follow.
    """

    response = model.generate_content(prompt)

    # Return the text reply without markdown symbols
    return response.text.replace('*', '')

if __name__ == "__main__":
    disease = input("Enter the disease name: ")
    remedies = get_home_remedies(disease)
    print("\nHome Remedies:")
    print(remedies)
