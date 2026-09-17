import os
from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response

def favicon_view(request):
    """Return 204 No Content for /favicon.ico."""
    return HttpResponse(status=204)

def page_view(request, page_name="index.html"):
    """
    Renders existing Jinja2/Django templates with necessary context
    such as the Google Maps API Key.
    """
    if not page_name:
        page_name = "index.html"
    elif not page_name.endswith(".html"):
        page_name = f"{page_name}.html"

    template_file = settings.BASE_DIR / 'templates' / page_name
    if not template_file.exists():
        raise Http404(f"Page '{page_name}' was not found.")

    context = {
        "google_maps_api_key": settings.GOOGLE_MAPS_API_KEY
    }
    return render(request, page_name, context)

from drf_spectacular.utils import extend_schema

@extend_schema(exclude=True)
@api_view(['GET'])
def api_root_view(request):
    """
    Overview of all available MEDiWiSE Django REST Backend endpoints.
    """
    return Response({
        "service": "MEDiWiSE - Digital Health Assistant REST API",
        "version": "1.0.0",
        "documentation": {
            "swagger_ui": "/api/docs/",
            "swagger_ui_alias": "/api/swagger/",
            "redoc": "/api/redoc/",
            "openapi_schema": "/api/schema/"
        },
        "endpoints": {
            "symptom_prediction": {
                "url": "/api/predict_symptoms/",
                "method": "POST",
                "description": "Predicts disease from a list of symptoms using Random Forest ML model.",
                "sample_payload": {"symptoms": ["headache", "fever", "nausea"]}
            },
            "skin_disease_prediction": {
                "url": "/api/predict_skin/",
                "method": "POST (multipart/form-data)",
                "description": "Classifies skin condition from an uploaded image using PyTorch EfficientNet-B0 DL model.",
                "sample_field": "image (file binary)"
            },
            "remedies_suggestion": {
                "url": "/api/get_remedies/",
                "method": "POST",
                "description": "Provides natural home remedies for conditions using Gemini AI.",
                "sample_payload": {"disease": "Common Cold"}
            },
            "health_chatbot": {
                "url": "/api/chat/",
                "method": "POST",
                "description": "Interactive conversational health assistant (MedTed) powered by Gemini AI.",
                "sample_payload": {"message": "How do I relieve back pain?"}
            }
        }
    })
