from django.db import models

# Create your models here.
class Localization(models.Model):
    ip = models.CharField(max_length=30)
    continent_code = models.CharField(max_length=5)
    continent_name = models.CharField(max_length=20)
    country_code = models.CharField(max_length=5)
    country_name = models.CharField(max_length=20)
    region_code = models.CharField(max_length=5)
    region_name = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    zip_code = models.CharField(max_length=20)
    latitude = models.FloatField(default=None)
    longitude = models.FloatField(default=None)