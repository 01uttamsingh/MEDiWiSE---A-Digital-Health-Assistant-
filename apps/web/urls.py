from django.urls import path, re_path
from .views import page_view, favicon_view, api_root_view

urlpatterns = [
    path('favicon.ico', favicon_view, name='favicon'),
    path('api/', api_root_view, name='api-root'),
    path('', page_view, {'page_name': 'index.html'}, name='home'),
    re_path(r'^(?P<page_name>[\w\-]+(?:\.html)?)$', page_view, name='page-view'),
]
