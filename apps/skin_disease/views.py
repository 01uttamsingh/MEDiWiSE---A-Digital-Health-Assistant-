from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiTypes
from .serializers import SkinDiseaseRequestSerializer, SkinDiseaseResponseSerializer
from .services import SkinDiseasePredictionService

class SkinDiseasePredictAPIView(APIView):
    """
    API endpoint for skin condition prediction using PyTorch EfficientNet-B0 model.
    """
    parser_classes = [MultiPartParser, FormParser]

    @extend_schema(
        tags=['Deep Learning - Skin Disease'],
        summary='Classify skin condition from image',
        description=(
            'Upload a photo of the affected skin area (JPEG/PNG). The deep learning model '
            '(PyTorch EfficientNet-B0) classifies the condition among 7 classes: '
            'Atopic Dermatitis (AD), Contact Dermatitis (CD), Eczema (EC), Scabies (SC), '
            'Seborrheic Dermatitis (SD), Tinea Corporis (TC), or Out-Of-Distribution (OOD).'
        ),
        request=SkinDiseaseRequestSerializer,
        responses={
            200: SkinDiseaseResponseSerializer,
            400: OpenApiTypes.OBJECT,
            500: OpenApiTypes.OBJECT,
        },
        examples=[
            OpenApiExample(
                'Successful Skin Prediction',
                value={
                    'disease': 'Atopic Dermatitis',
                    'confidence': '89.75%',
                    'precautions': ['Consult a dermatologist and keep the area clean.']
                },
                response_only=True
            ),
            OpenApiExample(
                'Out of Distribution (No Disease Detected)',
                value={
                    'disease': 'No disease predicted! (Check again, photo may be inappropriate)',
                    'confidence': '98.50%',
                    'precautions': 'Nothing to be display'
                },
                response_only=True
            )
        ]
    )
    def post(self, request, *args, **kwargs):
        if 'image' not in request.FILES and 'image' not in request.data:
            return Response(
                {"error": "No image file provided."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = SkinDiseaseRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"error": "Invalid image file provided.", "details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        image_file = serializer.validated_data['image']
        try:
            image_bytes = image_file.read()
            if not image_bytes:
                return Response(
                    {"error": "Uploaded image file is empty."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            service = SkinDiseasePredictionService.get_instance()
            result = service.predict(image_bytes)

            status_code = result.pop("status_code", status.HTTP_200_OK)
            return Response(result, status=status_code)

        except Exception as e:
            return Response(
                {"error": "An internal server error occurred while processing the image."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
