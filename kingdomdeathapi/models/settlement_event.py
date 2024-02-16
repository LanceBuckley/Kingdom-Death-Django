from django.db import models

class SettlementEvent(models.Model):
    settlement = models.ForeignKey("Settlement", on_delete=models.CASCADE, related_name="event")
    event = models.ForeignKey("Event", on_delete=models.CASCADE, related_name="affected_settlement")
    year = models.IntegerField()