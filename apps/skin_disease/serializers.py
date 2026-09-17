from rest_framework import serializers

class SkinDiseaseRequestSerializer(serializers.Serializer):
    image = serializers.ImageField(
        required=True,
        help_text="Image file of the skin affected area (JPEG, PNG, etc.)"
    )

class SkinDiseaseResponseSerializer(serializers.Serializer):
    disease = serializers.CharField(help_text="Detected skin disease name")
    confidence = serializers.CharField(help_text="Prediction confidence percentage")
    precautions = serializers.CharField(help_text="Precaution or guidance text / list")
