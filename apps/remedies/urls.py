from django.urls import re_path
from .views import RemediesAPIView

urlpatterns = [
    re_path(r'^get_remedies/?$', RemediesAPIView.as_view(), name='get-remedies'),
]
