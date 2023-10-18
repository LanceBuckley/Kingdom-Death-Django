from django.db import models

class ResourceType(models.Model):
    name = models.CharField(max_length=50)