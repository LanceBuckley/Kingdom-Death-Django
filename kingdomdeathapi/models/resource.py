from django.db import models

class Resource(models.Model):
    name = models.CharField(max_length=50)
    type = models.ForeignKey("ResourceType", on_delete=models.CASCADE, related_name="applicable_resource")