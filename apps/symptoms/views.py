from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiTypes
from .serializers import SymptomPredictionRequestSerializer, SymptomPredictionResponseSerializer
from .services import SymptomPredictorService

class SymptomPredictAPIView(APIView):
    """
    API endpoint for symptom-based disease prediction using Random Forest classifier.
    """
    parser_classes = [JSONParser]

    @extend_schema(
        tags=['Machine Learning - Symptoms'],
        summary='Predict disease from patient symptoms',
        description='Evaluates a list of reported symptoms with a pre-trained Random Forest ML model, returning predicted disease, confidence percentage, and recommended precautions.',
        request=SymptomPredictionRequestSerializer,
        responses={
            200: SymptomPredictionResponseSerializer,
            400: OpenApiTypes.OBJECT,
            500: OpenApiTypes.OBJECT,
        },
        examples=[
            OpenApiExample(
                'Standard Symptoms Request',
                value={'symptoms': ['itching', 'skin_rash', 'nodal_skin_eruptions']},
                request_only=True
            ),
            OpenApiExample(
                'Successful Prediction Result',
                value={
                    'disease': 'Fungal infection',
                    'accuracy': '92.50%',
                    'precautions': [
                        'bath twice',
                        'use dettol or neem in bathing water',
                        'keep infected area dry',
                        'use clean cloths'
                    ]
                },
                response_only=True
            )
        ]
    )
    def post(self, request, *args, **kwargs):
        serializer = SymptomPredictionRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"error": "Invalid input format. 'symptoms' must be a non-empty list of strings.", "details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        symptoms = serializer.validated_data['symptoms']
        service = SymptomPredictorService.get_instance()
        result = service.predict(symptoms)

        status_code = result.pop("status_code", status.HTTP_200_OK)

        if "error" in result:
            return Response(result, status=status_code)

        return Response(result, status=status.HTTP_200_OK)
