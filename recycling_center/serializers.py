from rest_framework import serializers

from recycling_center.models import RecyclingCenter, ItemRecycled

class RecyclingCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecyclingCenter
        fields = ['id', 'name', 'address', 'number', 'updated_by', 'created_by']
        
        extra_kwargs = {
            'created_by': {'write_only': True},
            'updated_by': {'write_only': True},
        }
        
class ItemRecycledSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemRecycled
        fields = ['id', 'product', 'recyclingcenter', 'target', 'recycled', 'brand', 'updated_by', 'created_by']
        
        extra_kwargs = {
            'created_by': {'write_only': True},
            'updated_by': {'write_only': True},
        }
        
class ItemRecycledListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemRecycled
        fields = ['id', 'product', 'recyclingcenter', 'target', 'recycled', 'brand']
        depth = 1