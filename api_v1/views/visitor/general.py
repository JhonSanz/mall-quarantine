""" General visitor api endpoints """

from cerberus import Validator
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from ...models.visitor import Visitor
from ...serializers.visitor import VisitorSerializer


class VisitorApi(APIView):
    """ GET and POST http verbs """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        """
        validator = Validator({
            "name": {"required": True, "empty": False, "type": "string"},
            "email": {
                "required": True, "empty": False, "type": "string",
                "regex": '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'}
        })
        if not validator.validate(request.data):
            return Response({
                "code": "invalid_body",
                "detail": "Invalid request data",
                "data": validator.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = VisitorSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                "code": "invalid_body",
                "detail": "There was and error creating a visitor instance",
                "data": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer.create(validated_data=request.data)
        return Response(status=status.HTTP_200_OK)
