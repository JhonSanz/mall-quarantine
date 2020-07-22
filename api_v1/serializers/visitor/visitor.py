""" Visitor model serializer """

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from ...models.visitor import Visitor


class VisitorSerializer(serializers.ModelSerializer):
    """ Defines visitor serializer from model definition """

    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=Visitor.objects.all())])

    class Meta:
        model = Visitor
        fields = ["pk", "name", "email", "created_at"]
