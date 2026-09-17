from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiTypes
from .serializers import RemediesRequestSerializer, RemediesResponseSerializer
from .services import RemediesService

class RemediesAPIView(APIView):
    """
    API endpoint for getting home remedies suggestions using Gemini AI.
    """
    parser_classes = [JSONParser]

    @extend_schema(
        tags=['AI Services - Remedies'],
        summary='Generate natural home remedies',
        description='Asks Google Gemini AI to generate 3-5 simple, practical home remedies and lifestyle measures for a given condition.',
        request=RemediesRequestSerializer,
        responses={
            200: RemediesResponseSerializer,
            400: OpenApiTypes.OBJECT,
        },
        examples=[
            OpenApiExample(
                'Remedies Request',
                value={'disease': 'Common Cold'},
                request_only=True
            ),
            OpenApiExample(
                'Remedies Response',
                value={'remedies': '1. Drink warm honey and ginger tea.\n2. Inhale steam.\n3. Get plenty of bed rest.\n\nIs there any other disease I can help you with?'},
                response_only=True
            )
        ]
    )
    def post(self, request, *args, **kwargs):
        serializer = RemediesRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"error": "Please provide a valid 'disease' parameter.", "details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        disease = serializer.validated_data['disease']
        service = RemediesService.get_instance()
        result = service.get_remedies(disease)

        return Response(result, status=status.HTTP_200_OK)
