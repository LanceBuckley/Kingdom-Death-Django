from django.db import models

class AchievedMilestone(models.Model):
    settlement = models.ForeignKey("Settlement", on_delete=models.CASCADE, related_name="milestones")
    milestone = models.ForeignKey("Milestone", on_delete=models.CASCADE, related_name="achievements")
    reached = models.BooleanField(default=False)