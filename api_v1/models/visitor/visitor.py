""" Contains the visitor model """

from django.db import models


class Visitor(models.Model):
    """ Category model definition """

    name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    temperature = models.FloatField(default=36.1)
    date_visited = models.DateTimeField(auto_now=True)
    enabled = models.BooleanField(default=True)

    class Meta:  # pylint: disable=too-few-public-methods
        """ Sets human readable name """
        verbose_name = "Visitante"

    def get_visitor_info(self):
        """ Returns basic visitor info """
        return "{} {}°C".format(self.name, self.temperature)

    def __str__(self):
        return self.name
