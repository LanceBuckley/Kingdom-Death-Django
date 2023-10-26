from django.db import models

class Disorder(models.Model):
    name = models.CharField(max_length=50)