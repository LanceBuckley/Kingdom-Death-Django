from django.db import models

class Resource(models.Model):
    name = models.CharField(max_length=50)
    type = models.ForeignKey("ResourceType", on_delete=models.CASCADE, related_name="applicable_resource")
    monster = models.BooleanField(default=False)
    strange = models.BooleanField(default=False)
    indomitable = models.BooleanField(default=False)
    vermin = models.BooleanField(default=False)
    monster_origin = models.ForeignKey("Monster", on_delete=models.CASCADE, related_name="droppable_resource", null=True)
    expansion = models.ForeignKey("ExpansionType", on_delete=models.CASCADE, related_name="expansion_resource", null=True)
    flavor_text = models.CharField(max_length=50)
    effect = models.CharField(max_length=50)