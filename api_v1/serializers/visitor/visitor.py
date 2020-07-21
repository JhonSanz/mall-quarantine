""" Visitor model serializer """

from rest_framework import serializers
from ...models.visitor import Visitor


class VisitorSerializer(serializers.ModelSerializer):
    """ Defines visitor serializer from model definition """

    class Meta:
        model = Visitor
        fields = ["pk", "name", "email", "temperature", "date_visited"]
