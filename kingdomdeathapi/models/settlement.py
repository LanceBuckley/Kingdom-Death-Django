from django.db import models

class Settlement(models.Model):
    name = models.CharField(max_length=50)
    survival_limit = models.IntegerField(min_length=0, max_length=50)
    population = models.IntegerField(min_length=0, max_length=50)
    game_master = models.ForeignKey("Player", on_delete=models.CASCADE, related_name="settlements")