from django.db import models

class WeaponProficiency(models.Model):
    name = models.CharField(max_length=50)
    specialist_effect = models.CharField(max_length=50)
    master_effect = models.CharField(max_length=50)
    expansion = models.ForeignKey("ExpansionType", on_delete=models.CASCADE, related_name="expansion_weapon_proficiency", null=True)
    