from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiTypes
from .serializers import ChatMessageRequestSerializer, ChatMessageResponseSerializer
from .services import ChatbotService

class ChatAPIView(APIView):
    """
    API endpoint for interactive health conversations with MedTed AI assistant.
    """
    parser_classes = [JSONParser]

    @extend_schema(
        tags=['AI Services - Chatbot'],
        summary='Chat with MedTed AI health assistant',
        description='Send health queries to MedTed, an empathetic and professional AI assistant powered by Google Gemini, for general wellness information and guidance.',
        request=ChatMessageRequestSerializer,
        responses={
            200: ChatMessageResponseSerializer,
            400: OpenApiTypes.OBJECT,
        },
        examples=[
            OpenApiExample(
                'Health Query Example',
                value={'message': 'How can I relieve a tension headache without medicines?'},
                request_only=True
            ),
            OpenApiExample(
                'MedTed Response Example',
                value={'response': 'To help relieve a tension headache naturally, try resting in a quiet, dimly lit room, gently massaging your temples and neck muscles, placing a warm or cool compress across your forehead, and drinking water.'},
                response_only=True
            )
        ]
    )
    def post(self, request, *args, **kwargs):
        serializer = ChatMessageRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"error": "Invalid request payload.", "details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        user_message = serializer.validated_data.get('message', '').strip()
        if not user_message:
            return Response({"response": "Please type a message."}, status=status.HTTP_200_OK)

        service = ChatbotService.get_instance()
        bot_response = service.get_chat_response(user_message)

        return Response({"response": bot_response}, status=status.HTTP_200_OK)
