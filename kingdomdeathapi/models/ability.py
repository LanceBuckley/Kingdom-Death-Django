from django.db import models

class Ability(models.Model):
    name = models.CharField(max_length=50)
    effect = models.CharField(max_length=50)
    expansion = models.ForeignKey("ExpansionType", on_delete=models.CASCADE, related_name="expansion_ability", null=True)