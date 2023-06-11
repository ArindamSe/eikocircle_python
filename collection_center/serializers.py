from rest_framework import serializers

from collection_center.models import CollectionCenter
from Item_collected.serializers import ItemCollectedListSerializer
from Item_collected.models import ItemCollected

class CollectionCenterSerializer(serializers.ModelSerializer):
    item_collected = serializers.SerializerMethodField()
    
    def get_item_collected(self, obj):
        data = ItemCollected.objects.filter(collectioncenter=obj)
        return ItemCollectedListSerializer(data, many=True).data
    
    class Meta:
        model = CollectionCenter
        fields = ['id', 'name', 'address', 'number', 'medium', 'city', 'item_collected', 'created_by', 'updated_by']
        
        extra_kwargs = {
            'created_by': {'write_only': True},
            'updated_by': {'write_only': True},
        }
    