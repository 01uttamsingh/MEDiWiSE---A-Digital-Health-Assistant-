from django.test import TestCase, Client
from rest_framework import status

class WebAndRootAPITests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_api_root_overview(self):
        response = self.client.get('/api/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIn("documentation", data)
        self.assertIn("endpoints", data)
        self.assertIn("symptom_prediction", data["endpoints"])
        self.assertIn("skin_disease_prediction", data["endpoints"])
        self.assertIn("remedies_suggestion", data["endpoints"])
        self.assertIn("health_chatbot", data["endpoints"])

    def test_swagger_schema_endpoint(self):
        response = self.client.get('/api/schema/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_swagger_ui_endpoint(self):
        response = self.client.get('/api/docs/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_swagger_ui_alias_endpoint(self):
        response = self.client.get('/api/swagger/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_redoc_ui_endpoint(self):
        response = self.client.get('/api/redoc/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_home_page_renders(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_ml_predict_page_renders(self):
        response = self.client.get('/ml_predict.html')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_dl_predict_page_renders(self):
        response = self.client.get('/dl_predict.html')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_chat_page_renders(self):
        response = self.client.get('/chat.html')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_remedies_page_renders(self):
        response = self.client.get('/remedies.html')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_favicon_204(self):
        response = self.client.get('/favicon.ico')
        self.assertEqual(response.status_code, 204)
