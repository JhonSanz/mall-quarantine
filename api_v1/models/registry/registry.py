""" Contains the visitor model """

from django.db import models
from ..visitor import Visitor
from ..mall import Mall

class Registry(models.Model):
    """ Registry model definition """

    visitor = models.ForeignKey(Visitor)
    mall = models.ForeignKey(Mall)
    temperature = models.FloatField(default=36.1)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:  # pylint: disable=too-few-public-methods
        """ Sets human readable name """
        verbose_name = "Visitante"

    def get_visitor_info(self):
        """ Returns basic visitor info """
        return "{} {}°C".format(self.name, self.temperature)

    def __str__(self):
        return self.name
