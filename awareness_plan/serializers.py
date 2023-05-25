from rest_framework import serializers

from awareness_plan.models import AwarenessPlan, AwarenessPlanPics
from awareness_plan_metrics.models import AwarenessPlanMetrics
from awareness_plan_metrics.serializers import AwarenessPlanMetricsListSerializer

class AwarenessPlanPicsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AwarenessPlanPics
        fields = ['id', 'awarenessplan', 'pics', 'created_by', 'updated_by']

        extra_kwargs = {
            'created_by': {'write_only': True},
            'updated_by': {'write_only': True},
        }
class AwarenessPlanListSerializer(serializers.ModelSerializer):
    pics = serializers.SerializerMethodField()
    metrics = serializers.SerializerMethodField()
    
    def get_pics(self, obj):
        data = AwarenessPlanPics.objects.filter(awarenessplan=obj)
        return AwarenessPlanPicsSerializer(data, many=True).data
    
    def get_metrics(self, obj):
        data = AwarenessPlanMetrics.objects.filter(awarenessplan=obj)
        return AwarenessPlanMetricsListSerializer(data, many=True).data
    class Meta:
        model = AwarenessPlan
        fields = ['id', 'product', 'theme', 'medium', 'city', 'date', 'communication', 'target_audience', 'brand', 'pics', 'metrics']
        depth = 2
class AwarenessPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = AwarenessPlan
        fields = ['id', 'product', 'theme', 'medium', 'city', 'date', 'communication', 'target_audience', 'brand', 'created_by', 'updated_by']
        
        extra_kwargs = {
            'created_by': {'write_only': True},
            'updated_by': {'write_only': True},
        }
        
    def save(self, **kwargs):
        awarenessplan = super().save()
        pics = self.context.get('pics')
        
        if pics:
            files = [
                AwarenessPlanPics(awarenessplan=awarenessplan, pics=file) for file in pics
            ]
            AwarenessPlan.objects.bulk_create(files)
        
        return awarenessplan
    