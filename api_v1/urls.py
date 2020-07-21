from django.urls import path
from .views.visitor import VisitorApi

app_name = "api_v1"
urlpatterns = [
    path('visitor', VisitorApi.as_view()),
]
