from rest_framework import serializers

class RemediesRequestSerializer(serializers.Serializer):
    disease = serializers.CharField(
        required=True,
        allow_blank=False,
        trim_whitespace=True,
        help_text="Name of the disease or condition to fetch remedies for"
    )

class RemediesResponseSerializer(serializers.Serializer):
    remedies = serializers.CharField(help_text="Remedies text suggestions")
