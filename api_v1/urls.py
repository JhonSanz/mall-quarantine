from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from .views.visitor import VisitorApi
from .views.registry import RegistryApi
from .views.mall import MallApi

app_name = "api_v1"
urlpatterns = [
    path('mall', MallApi.as_view(), name="mall_general"),
    path('registry', RegistryApi.as_view(), name="registry_general"),
    path('visitor', VisitorApi.as_view(), name="visitor_general"),
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]
