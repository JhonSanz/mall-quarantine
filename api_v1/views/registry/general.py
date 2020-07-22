""" """

from datetime import datetime
from cerberus import Validator, schema
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


class RegistryApi(APIView):
    """ """

    def post(self, request):
        """
        """
        validator = Validator({
            "mall": {"required": True, "empty": False, "type": "string"},
            "email": {
                "required": True, "empty": False, "type": "string",
                "regex": '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'},
            "temperature": {"required": True, "empty": False,
                            "type": "number"}
        })
        if not validator.validate(request.data):
            return Response({
                "code": "invalid_body",
                "detail": "Invalid request data",
                "data": validator.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        visitor_instance = Visitor.objects.filter(
            email=request.data.get("email"))
        mall_instance = Mall.objects.filter(name=request.data.get("mall"))
        if not visitor_instance.exists() or not mall_instance.exists():
            return Response({
                "code": ("visitor_not_found" if not visitor_instance.exists()
                         else "mall_not_found"),
                "detail": "Requested dependency was not found"
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = VisitorSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                "code": "invalid_body",
                "detail": "There was and error creating a visitor instance",
                "data": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        instance = serializer.create(validated_data=request.data)
        if temperature > 38:
            instance.enabled = False
            instance.save()
            return Response({
                "code": "dangerous_visitor",
                "detail": "You are sick, go home and rest"
            }, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_200_OK)