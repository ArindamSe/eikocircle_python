from django.db import models

from Common.models import Common
from awareness_plan.models import AwarenessPlan

class AwarenessPlanMetrics(Common):
    awarenessplan = models.ForeignKey(AwarenessPlan, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    number_of_themes = models.IntegerField(null=True, blank=True)
    number_of_life_touched = models.IntegerField(null=True, blank=True)
    total_duration = models.CharField(max_length=100, null=True, blank=True)
    targeted_demographics = models.CharField(max_length=200, null=True, blank=True)
    targeted_interest = models.CharField(max_length=200, null=True, blank=True)
    
    class Meta:
        db_table="Awareness Plan Metrics"
        
    def __str__(self):
        return f"{self.awarenessplan.theme}-{self.name}"
    