from django.db import models

class Milestone(models.Model):
    type = models.CharField(max_length=50)