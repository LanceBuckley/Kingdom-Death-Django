from django.db import models

class Monster(models.Model):
    name = models.CharField(max_length=50)
    expansion = models.ForeignKey("ExpansionType", on_delete=models.CASCADE, related_name="expansion_monster", null=True)
    nemesis = models.BooleanField(default=False)
    core = models.BooleanField(default=False)
    legendary = models.BooleanField(default=False)
    