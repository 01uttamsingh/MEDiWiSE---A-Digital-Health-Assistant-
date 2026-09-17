from django.urls import re_path
from .views import SymptomPredictAPIView

urlpatterns = [
    re_path(r'^predict_symptoms/?$', SymptomPredictAPIView.as_view(), name='predict-symptoms'),
]
