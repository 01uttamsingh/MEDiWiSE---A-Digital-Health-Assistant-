import json
from unittest.mock import patch
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

class RemediesAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('get-remedies')

    def test_get_remedies_no_disease(self):
        payload = {"disease": "no"}
        response = self.client.post(self.url, data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data.get("remedies"), "Wish you for a better health! Take care")

    def test_get_remedies_missing_payload(self):
        payload = {}
        response = self.client.post(self.url, data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('apps.remedies.services.genai.GenerativeModel')
    def test_get_remedies_with_mock_gemini(self, mock_model_class):
        mock_instance = mock_model_class.return_value
        mock_instance.generate_content.return_value.text = "1. Drink honey and lemon tea.\n2. Rest well."

        payload = {"disease": "Cough"}
        response = self.client.post(self.url, data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIn("remedies", data)
        self.assertIn("honey and lemon", data["remedies"])
