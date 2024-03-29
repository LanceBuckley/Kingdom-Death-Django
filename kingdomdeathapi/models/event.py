from django.db import models

class Event(models.Model):
    name = models.CharField(max_length=50)
    effect = models.CharField(max_length=50)
    story = models.BooleanField(default=False)
    campaign = models.ForeignKey("Campaign", on_delete=models.CASCADE, related_name="campaign_event", null=True)
    expansion = models.ForeignKey("ExpansionType", on_delete=models.CASCADE, related_name="expansion_event", null=True)