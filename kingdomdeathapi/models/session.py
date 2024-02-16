from django.db import models

class Session(models.Model):
    host = models.ForeignKey("Player", on_delete=models.CASCADE, related_name="hosting_session")
    settlement = models.ForeignKey("Settlement", on_delete=models.CASCADE, related_name="in_session")
    players = models.ManyToManyField("Player", related_name="participating")