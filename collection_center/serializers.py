from rest_framework import serializers

from collection_center.models import CollectionCenter, CollectedCenterItemCollected
from Item_collected.models import ItemCollected

class CollectionCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectionCenter
        fields = ['id', 'name', 'address', 'number', 'medium', 'city', 'created_by', 'updated_by']
        
        extra_kwargs = {
            'created_by': {'write_only': True},
            'updated_by': {'write_only': True},
        }
        
    def save(self, **kwargs):
        collection_center = super().save()
        item_collected_ids = self.context.get('item_collected')
        
        if item_collected_ids:
            item_collected = ItemCollected.objects.filter(id__in=item_collected_ids)
            colletectioncenteritemcollected = [
                CollectedCenterItemCollected(collection_center=collection_center, item_collected=item) for item in item_collected
            ]
            CollectedCenterItemCollected.objects.bulk_create(colletectioncenteritemcollected)
            
        return collection_center