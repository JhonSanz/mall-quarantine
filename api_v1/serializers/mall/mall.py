""" Mall model serializer """

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from ...models.mall import Mall


class MallSerializer(serializers.ModelSerializer):
    """ Defines Mall serializer from model definition """

    name = serializers.CharField(
        validators=[UniqueValidator(queryset=Mall.objects.all())])

    class Meta:
        model = Mall
        fields = ["pk", "name"]
