import logging
import google.generativeai as genai
from django.conf import settings

logger = logging.getLogger(__name__)

class ChatbotService:
    """
    Service managing MedTed conversational AI assistant via Google Gemini.
    """
    _instance = None

    def __init__(self):
        self.model_name = "models/gemini-2.5-flash"

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def get_chat_response(self, user_message: str) -> str:
        """
        Generate empathetic, informative health guidance response for user message.
        """
        if not user_message or not user_message.strip():
            return "Please type a message."

        if not settings.GEMINI_API_KEY:
            return "Gemini API key is not configured. Please set GEMINI_API_KEY in your .env file."

        try:
            model = genai.GenerativeModel(self.model_name)
            prompt = (
                "You are MedTed, a professional and empathetic AI health assistant. "
                "Respond clearly, politely, and concisely. "
                f'User says: "{user_message.strip()}". '
                "Give helpful general health information, but strictly avoid giving medical advice or diagnoses."
            )
            response = model.generate_content(prompt)
            return response.text.replace('*', '').strip()

        except Exception as e:
            logger.error(f"Error during Gemini API call for chatbot: {e}", exc_info=True)
            return "Sorry, I'm having trouble connecting right now. Please try again later."
