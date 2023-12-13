from django.db import models

class Milestone(models.Model):
    settlement = models.ForeignKey("Settlement", on_delete=models.CASCADE, related_name="achieved_milestone")
    milestone_type = models.ForeignKey("MilestoneType", on_delete=models.CASCADE, related_name="achievements")
    achieved = models.BooleanField(default=False)
    