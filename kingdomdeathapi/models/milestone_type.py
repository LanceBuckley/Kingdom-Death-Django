from django.db import models

class MilestoneType(models.Model):
    type = models.CharField(max_length=50)
    