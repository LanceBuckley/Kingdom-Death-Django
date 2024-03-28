from django.db import models

class ExpansionType(models.Model):
    name = models.CharField(max_length=50)
    