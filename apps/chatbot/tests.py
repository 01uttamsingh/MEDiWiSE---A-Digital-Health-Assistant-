import json
from unittest.mock import patch
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

class ChatbotAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('chat')

    def test_chat_empty_message(self):
        payload = {"message": ""}
        response = self.client.post(self.url, data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data.get("response"), "Please type a message.")

    @patch('apps.chatbot.services.genai.GenerativeModel')
    def test_chat_with_mock_gemini(self, mock_model_class):
        mock_instance = mock_model_class.return_value
        mock_instance.generate_content.return_value.text = "Hello! I am MedTed. Stay hydrated."

        payload = {"message": "Hello, I feel dehydrated."}
        response = self.client.post(self.url, data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIn("response", data)
        self.assertIn("MedTed", data["response"])
