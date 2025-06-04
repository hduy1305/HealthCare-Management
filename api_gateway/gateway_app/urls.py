from django.urls import path, re_path
from .views import ProxyView
from .views import home

urlpatterns = [
    path('', home),
    re_path(r'^(?P<service_name>[\w-]+)/(?P<path>.*)$', ProxyView.as_view()),
]
