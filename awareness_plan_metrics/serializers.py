from rest_framework import serializers

from awareness_plan_metrics.models import AwarenessPlanMetrics

class AwarenessPlanMetricsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = AwarenessPlanMetrics
        fields = ['id', 'awarenessplan', 'name', 'number_of_themes', 'number_of_life_touched', 'total_duration', 'targeted_demographics', 'targeted_interest']
        
class AwarenessPlanMetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AwarenessPlanMetrics
        fields = ['id', 'awarenessplan', 'name', 'number_of_themes', 'number_of_life_touched', 'total_duration', 'targeted_demographics', 'targeted_interest', 'created_by', 'updated_by']
        
        extra_kwargs = {
            'created_by': {'write_only': True},
            'updated_by': {'write_only': True},
        }