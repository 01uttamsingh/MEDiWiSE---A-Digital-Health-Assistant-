from django.urls import re_path
from .views import SkinDiseasePredictAPIView

urlpatterns = [
    re_path(r'^predict_skin/?$', SkinDiseasePredictAPIView.as_view(), name='predict-skin'),
]
