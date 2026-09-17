from django.urls import re_path
from .views import ChatAPIView

urlpatterns = [
    re_path(r'^chat/?$', ChatAPIView.as_view(), name='chat'),
]
