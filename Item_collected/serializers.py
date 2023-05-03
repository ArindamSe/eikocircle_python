from rest_framework import serializers

from Item_collected.models import ItemCollected, ItemCollectedPictures

class ItemCollectedList(serializers.ModelSerializer):
    class Meta:
        model = ItemCollected
        fields = ['id', 'product', 'weight']
        depth = 1
        
class ItemCollected(serializers.ModelSerializer):
    class Meta:
        model = ItemCollected
        fields = ['id', 'product', 'weight', 'created_by', 'updated_by']
        
        extra_kwargs = {
            'created_by': {'write_only': True},
            'updated_by': {'write_only': True},
        }
        
    