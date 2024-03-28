from django.db import models

class Impairment(models.Model):
    name = models.CharField(max_length=50)
    effect = models.CharField(max_length=50)