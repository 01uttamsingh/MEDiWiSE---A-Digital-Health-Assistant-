import io
from PIL import Image
from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APIClient

class SkinDiseaseAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('predict-skin')

    def _create_test_image(self):
        file_obj = io.BytesIO()
        image = Image.new('RGB', (224, 224), color=(73, 109, 137))
        image.save(file_obj, format='JPEG')
        file_obj.seek(0)
        return SimpleUploadedFile("test_skin.jpg", file_obj.read(), content_type="image/jpeg")

    def test_predict_skin_success(self):
        uploaded_image = self._create_test_image()
        response = self.client.post(
            self.url,
            {'image': uploaded_image},
            format='multipart'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIn("disease", data)
        self.assertIn("confidence", data)
        self.assertIn("precautions", data)

    def test_predict_skin_missing_image(self):
        response = self.client.post(self.url, {}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = response.json()
        self.assertIn("error", data)
