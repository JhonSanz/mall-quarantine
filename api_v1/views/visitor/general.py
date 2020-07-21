""" """

from cerberus import Validator
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from ...models.visitor import Visitor
from ...serializers.visitor import VisitorSerializer


class VisitorApi(APIView):
    """ """

    def get(self, request):
        """
        """
        validator = Validator({
            "name": {"required": False, "empty": False, "type": "string"}
            "email": {"required": False, "empty": False, "type": "string",
                      "regex": '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'}
            "temperature": {"required": False, "empty": False, "type": "number"}
            "date_visited": {
                "required": False, "empty": False, "type": "date"}
        })
        if not validator.validate(request.GET):
            return Response({
                "code": "invalid_filtering_params",
                "detail": "There was an error with your filtering params",
                "data": v/alidator.errors
            })

        filters = []
        if request.GET.get("name"):
            filters.append(Q(name=request.GET.get("name")))
        if request.GET.get("email"):
            filters.append(Q(email=request.GET.get("email")))
        if request.GET.get("temperature"):
            filters.append(Q(temperature=request.GET.get("temperature")))
        if request.GET.get("date_visited"):
            filters.append(Q(date_visited=request.GET.get("date_visited")))

        return Response(
            VisitorSerializer(Visitor.objects.filter(
                *filters), many=True).data,
            status=status.HTTP_200_OK)
