from rest_framework import serializers

from awareness_plan.models import AwarenessPlan, AwarenessPlanPics

class AwarenessPlanListSerializer(serializers.ModelSerializer):
    class Meta:
        model = AwarenessPlan
        fields = ['id', 'product', 'theme', 'medium', 'city', 'date', 'communication', 'target_audience']
        depth = 2
        
class AwarenessPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = AwarenessPlan
        fields = ['id', 'product', 'theme', 'medium', 'city', 'date', 'communication', 'target_audience', 'created_by', 'updated_by']
        
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