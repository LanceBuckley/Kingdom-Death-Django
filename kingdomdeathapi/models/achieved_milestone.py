from django.db import models

class AchievedMilestone(models.Model):
    settlement = models.ForeignKey("Settlement", on_delete=models.CASCADE, related_name="achieved_milestone")
    milestone_type = models.ForeignKey("MilestoneType", on_delete=models.CASCADE, related_name="achievements")
    reached = models.BooleanField(default=False)