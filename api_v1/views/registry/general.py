""" """

from datetime import timedelta, datetime
from cerberus import Validator
from django.db.models import Q
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from ...serializers.registry import RegistrySerializer
from ...models.visitor import Visitor
from ...models.mall import Mall
from ...models.registry import Registry


class RegistryApi(APIView):
    """ """

    permission_classes = [IsAuthenticated]

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
            "created_at": {
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
            filters.append(Q(visitor__name=request.GET.get("name")))
        if request.GET.get("email"):
            filters.append(Q(visitor__email=request.GET.get("email")))
        if request.GET.get("temperature"):
            filters.append(Q(temperature=request.GET.get("temperature")))
        if request.GET.get("created_at"):
            date_filter = request.GET.get("created_at").split("-")
            filters.append(Q(created_at__year=date_filter[0]))
            filters.append(Q(created_at__month=date_filter[1]))
            filters.append(Q(created_at__day=date_filter[-1]))

        return Response(
            RegistrySerializer(Registry.objects.filter(
                *filters), many=True).data,
            status=status.HTTP_200_OK)

    def post(self, request):
        """
        """
        validator = Validator({
            "malls": {
                "required": True, "empty": False, "type": "list",
                "schema": {"type": "number", "required": True,
                           "empty": False}
            },
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
            email=request.data.pop("email"))

        if(not visitor_instance.exists() or not
                all(map(lambda x: Mall.objects.filter(pk=x).exists(),
                        set(request.data.get("malls"))))):
            return Response({
                "code": ("visitor_not_found" if not visitor_instance.exists()
                         else "mall_not_found"),
                "detail": "Requested dependency was not found"
            }, status=status.HTTP_404_NOT_FOUND)

        if not visitor_instance.first().enabled:
            if timezone.now() - Registry.objects.filter(
                visitor=visitor_instance.first()).order_by(
                    "-created_at")[0].created_at > timedelta(days=6):
                visitor_instance.update(enabled=True)
            else:
                return Response({
                    "code": "dangerous_visitor",
                    "detail": "You are still sick, go home and rest",
                }, status=status.HTTP_400_BAD_REQUEST)

        serializer = RegistrySerializer(data={
            "visitor": visitor_instance.first().pk,
            **request.data})
        if not serializer.is_valid():
            return Response({
                "code": "invalid_body",
                "detail": "There was and error creating an instance",
                "data": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        instance = serializer.create(validated_data={
            "visitor": visitor_instance.first().pk,
            **request.data})
        if request.data.get("temperature") > 38:
            visitor_instance.update(enabled=False)
            return Response({
                "code": "dangerous_visitor",
                "detail": "You are sick, go home and rest"
            }, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_200_OK)
