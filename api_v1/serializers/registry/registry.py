""" Registry model serializer """

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from ...models.registry import Registry
from ...models.mall import Mall
from ...models.visitor import Visitor


class RegistrySerializer(serializers.ModelSerializer):
    """ Defines Registry serializer from model definition """

    class Meta:
        model = Registry
        fields = ["pk", "visitor", "mall", "temperature", "created_at"]

    def create(self, validated_data):
        return Registry.objects.create(
            mall=Mall.objects.get(pk=validated_data.pop("mall")),
            visitor=Visitor.objects.get(pk=validated_data.pop("visitor")),
            **validated_data)
