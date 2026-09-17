import logging
import google.generativeai as genai
from django.conf import settings

logger = logging.getLogger(__name__)

class RemediesService:
    """
    Service to generate home remedies using Google Gemini generative AI.
    """
    _instance = None

    def __init__(self):
        self.model_name = "models/gemini-2.5-flash"

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def get_remedies(self, disease_name: str) -> dict:
        """
        Generate 3-5 simple home remedies for a specified condition or disease.
        """
        if not disease_name or not disease_name.strip():
            return {"remedies": "Please enter a disease name."}

        cleaned_disease = disease_name.strip()
        if cleaned_disease.lower() in ['no', 'none', 'nothing', 'quit', 'exit']:
            return {"remedies": "Wish you for a better health! Take care"}

        if not settings.GEMINI_API_KEY:
            return {
                "remedies": "Gemini API key is not configured. Please set GEMINI_API_KEY in your .env file."
            }

        try:
            model = genai.GenerativeModel(self.model_name)
            prompt = (
                f"You are a friendly health assistant. Suggest 3 to 5 simple home remedies for '{cleaned_disease}'. "
                "Keep instructions clear, simple, and easy to follow. "
                "Format as a simple text list without intro/conclusion. Do not use markdown."
            )
            response = model.generate_content(prompt)
            remedies_text = response.text.replace('*', '').replace('•', '').strip()
            follow_up = "\n\nIs there any other disease I can help you with?"
            return {"remedies": remedies_text + follow_up}

        except Exception as e:
            logger.error(f"Error fetching remedies from Gemini API: {e}", exc_info=True)
            return {"remedies": "Sorry, I couldn't fetch remedies at the moment. Please try again later."}
