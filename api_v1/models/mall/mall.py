""" Contains the mall model """

from django.db import models


class Mall(models.Model):
    """ Mall model definition """

    name = models.CharField(max_length=45)

    class Meta:  # pylint: disable=too-few-public-methods
        """ Sets human readable name """
        verbose_name = "Centro Comercial"
        verbose_name_plural = "Centros Comerciales"

    def __str__(self):
        return self.name
