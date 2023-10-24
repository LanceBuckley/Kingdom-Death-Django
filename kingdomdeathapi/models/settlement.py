from django.db import models

class Settlement(models.Model):
    name = models.CharField(max_length=50)
    survival_limit = models.IntegerField()
    population = models.IntegerField()
    game_master = models.ForeignKey("Player", on_delete=models.CASCADE, related_name="settlements")