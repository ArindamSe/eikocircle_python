from django.db import models

from Common.models import Common
from awareness_plan.models import AwarenessPlan

class AwarenessPlanMetrics(Common):
    awarenessplan = models.ForeignKey(AwarenessPlan, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    proposed = models.IntegerField()
    impacted = models.IntegerField()
    
    class Meta:
        db_table="Awareness Plan Metrics"
        
    def __str__(self):
        return f"{self.awarenessplan}-{self.name}-{self.proposed}-{self.impacted}"
    