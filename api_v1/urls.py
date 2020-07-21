from django.urls import path
from .views.visitor import VisitorApi
from rest_framework_simplejwt.views import TokenObtainPairView


app_name = "api_v1"
urlpatterns = [
    path('visitor', VisitorApi.as_view(), name="visitor_general"),
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]
