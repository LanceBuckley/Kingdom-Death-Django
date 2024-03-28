from django.db import models

class Disorder(models.Model):
    name = models.CharField(max_length=50)
    flavor_text = models.CharField(max_length=50)
    effect = models.CharField(max_length=50)
    expansion = models.ForeignKey("ExpansionType", on_delete=models.CASCADE, related_name="expansion_disorder", null=True)