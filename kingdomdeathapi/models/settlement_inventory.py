from django.db import models

class SettlementInventory(models.Model):
    settlement = models.ForeignKey("Settlement", on_delete=models.CASCADE, related_name="inventory")
    resource = models.ForeignKey("Resource", on_delete=models.CASCADE, related_name="inventory")
    amount = models.IntegerField()