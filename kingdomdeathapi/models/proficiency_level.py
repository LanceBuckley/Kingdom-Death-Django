from django.db import models

class ProficiencyLevel(models.Model):
    name = models.CharField(max_length=50)
    weapon_type = models.ForeignKey("WeaponProficiency", on_delete=models.CASCADE, related_name="survivor_weapon_proficiency", null=True)
    survivor = models.ForeignKey("Survivor", on_delete=models.CASCADE, related_name="proficiency_level", null=True)
    level = models.IntegerField()
    