from django.db import models
from .utils import random_string


# Create your models here.
class TinyURL(models.Model):
    shortcode = models.CharField(
        primary_key=True,
        max_length=6,
        unique=True,
        default=random_string
    )
    url = models.URLField(unique=True)

    def __str__(self):
        return self.shortcode


class TinyURLStats(models.Model):
    shortcode = models.ForeignKey(TinyURL, on_delete=models.CASCADE)
    week = models.PositiveIntegerField()
    year = models.PositiveIntegerField()

    def __str__(self):
        return self.shortcode_id