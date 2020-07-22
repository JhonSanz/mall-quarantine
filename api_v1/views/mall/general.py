""" """

from cerberus import Validator
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from ...serializers.registry import RegistrySerializer
from ...models.mall import Mall


class MallApi(APIView):
    """ """

    def post(self, request):
        """
        """
        validator = Validator({
            "name": {"required": True, "empty": False, "type": "string"},
        })
        if not validator.validate(request.data):
            return Response({
                "code": "invalid_body",
                "detail": "Invalid request data",
                "data": validator.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        Mall.objects.create(**request.data)
        return Response(status=status.HTTP_200_OK)
