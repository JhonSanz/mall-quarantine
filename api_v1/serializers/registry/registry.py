""" Registry model serializer """

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from ...models.registry import Registry


class RegistrySerializer(serializers.ModelSerializer):
    """ Defines Registry serializer from model definition """

    class Meta:
        model = Registry
        fields = ["pk", "visitor", "mall", "temperature", "created_at"]
