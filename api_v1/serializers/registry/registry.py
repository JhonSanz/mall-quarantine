""" Registry model serializer """

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from ...models.registry import Registry
from ...models.mall import Mall
from ...models.visitor import Visitor
from ...serializers.mall import MallSerializer
from ...serializers.visitor import VisitorSerializer


class RegistrySerializer(serializers.ModelSerializer):
    """ Defines Registry serializer from model definition """

    visitor = VisitorSerializer(read_only=True)
    mall = MallSerializer(read_only=True, many=True)

    class Meta:
        model = Registry
        fields = ["pk", "visitor", "mall", "temperature", "created_at"]

    def create(self, validated_data):
        malls = validated_data.pop("malls")
        instance = Registry.objects.create(
            visitor=Visitor.objects.get(pk=validated_data.pop("visitor")),
            **validated_data)
        instance.mall.add(*malls)
        return instance
