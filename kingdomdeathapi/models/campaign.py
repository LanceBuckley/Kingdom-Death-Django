from django.db import models

class Campaign(models.Model):
    name = models.CharField(max_length=50)
    years = models.IntegerField()
    expansion = models.ForeignKey("ExpansionType", on_delete=models.CASCADE, related_name="expansion_campaign", null=True)