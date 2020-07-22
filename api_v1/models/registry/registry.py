""" Contains the visitor model """

from django.db import models
from ..visitor import Visitor
from ..mall import Mall

class Registry(models.Model):
    """ Registry model definition """

    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE)
    mall = models.ManyToManyField(Mall)
    temperature = models.FloatField(default=36.1)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:  # pylint: disable=too-few-public-methods
        """ Sets human readable name """
        verbose_name = "Visita"

    def __str__(self):
        return "{} -> {}".format(self.visitor.name, self.mall.name)
