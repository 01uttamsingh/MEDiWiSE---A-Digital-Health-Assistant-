import json
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

class SymptomPredictionAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('predict-symptoms')

    def test_predict_symptoms_success(self):
        payload = {
            "symptoms": ["back_pain", "abdominal_pain"]
        }
        response = self.client.post(self.url, data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIn("disease", data)
        self.assertIn("accuracy", data)
        self.assertIn("precautions", data)
        self.assertIsInstance(data["precautions"], list)

    def test_predict_symptoms_invalid_symptom(self):
        payload = {
            "symptoms": ["completely_unknown_fake_symptom_xyz"]
        }
        response = self.client.post(self.url, data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = response.json()
        self.assertIn("error", data)

    def test_predict_symptoms_empty_payload(self):
        payload = {
            "symptoms": []
        }
        response = self.client.post(self.url, data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
