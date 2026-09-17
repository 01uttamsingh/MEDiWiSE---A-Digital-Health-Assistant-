from rest_framework import serializers

class SymptomPredictionRequestSerializer(serializers.Serializer):
    symptoms = serializers.ListField(
        child=serializers.CharField(allow_blank=False, trim_whitespace=True),
        allow_empty=False,
        help_text="List of symptoms reported by the patient"
    )

class SymptomPredictionResponseSerializer(serializers.Serializer):
    disease = serializers.CharField(help_text="Predicted disease name")
    accuracy = serializers.CharField(help_text="Prediction confidence percentage")
    precautions = serializers.ListField(
        child=serializers.CharField(),
        help_text="Recommended precautions for the predicted disease"
    )
