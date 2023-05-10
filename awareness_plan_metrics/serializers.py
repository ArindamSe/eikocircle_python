from rest_framework import serializers

from awareness_plan_metrics.models import AwarenessPlanMetrics

class AwarenessPlanMetricsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = AwarenessPlanMetrics
        fields = ['id', 'awarenessplan', 'name', 'proposed', 'impacted']
        depth = 1
        
class AwarenessPlanMetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AwarenessPlanMetrics
        fields = ['id', 'awarenessplan', 'name', 'proposed', 'impacted', 'created_by', 'updated_by']
        
        extra_kwargs = {
            'created_by': {'write_only': True},
            'updated_by': {'write_only': True},
        }