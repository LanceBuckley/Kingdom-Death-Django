from django.db import models

class WeaponProficiency(models.Model):
    name = models.CharField(max_length=50)
    