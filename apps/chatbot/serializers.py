from rest_framework import serializers

class ChatMessageRequestSerializer(serializers.Serializer):
    message = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="User message sent to MedTed chatbot"
    )

class ChatMessageResponseSerializer(serializers.Serializer):
    response = serializers.CharField(help_text="MedTed chatbot AI response")
