""" """

from cerberus import Validator
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from ...serializers.mall import MallSerializer
from ...models.mall import Mall


class MallApi(APIView):
    """ """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        """
        return Response(
            MallSerializer(Mall.objects.all(), many=True).data,
            status=status.HTTP_200_OK)

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
