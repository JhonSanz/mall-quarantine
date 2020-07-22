""" General visitor api endpoints """

from datetime import datetime
from cerberus import Validator
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from ...models.visitor import Visitor
from ...serializers.visitor import VisitorSerializer


class VisitorApi(APIView):
    """ GET and POST http verbs """

    def get(self, request):
        """
        """

        def to_date(s): return datetime.strptime(s, '%Y-%m-%d')
        validator = Validator({
            "name": {"required": False, "empty": False, "type": "string"},
            "email": {
                "required": False, "empty": False, "type": "string",
                "regex": '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'},
            "temperature": {"required": False, "empty": False,
                            "type": "string"},
            "date_visited": {
                "required": False, "empty": False, "type": "date",
                "coerce": to_date}
        })
        if not validator.validate(request.GET):
            return Response({
                "code": "invalid_filtering_params",
                "detail": "There was an error with your filtering params",
                "data": validator.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        filters = []
        if request.GET.get("name"):
            filters.append(Q(name=request.GET.get("name")))
        if request.GET.get("email"):
            filters.append(Q(email=request.GET.get("email")))
        if request.GET.get("temperature"):
            filters.append(Q(temperature=request.GET.get("temperature")))
        if request.GET.get("date_visited"):
            date_filter = request.GET.get("date_visited").split("-")
            filters.append(Q(date_visited__year=date_filter[0]))
            filters.append(Q(date_visited__month=date_filter[1]))
            filters.append(Q(date_visited__day=date_filter[-1]))

        return Response(
            VisitorSerializer(Visitor.objects.filter(
                *filters), many=True).data,
            status=status.HTTP_200_OK)

    def post(self, request):
        """
        """
        validator = Validator({
            "name": {"required": True, "empty": False, "type": "string"},
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

        serializer = VisitorSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                "code": "invalid_body",
                "detail": "There was and error creating a visitor instance",
                "data": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        instance = serializer.create(validated_data=request.data)
        if request.data.get("temperature") > 38:
            instance.enabled = False
            instance.save()
            return Response({
                "code": "dangerous_visitor",
                "detail": "You are sick, go home and rest"
            }, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_200_OK)
