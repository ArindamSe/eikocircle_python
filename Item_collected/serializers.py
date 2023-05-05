from rest_framework import serializers

from Item_collected.models import ItemCollected, ItemCollectedPictures

class ItemCollectedListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemCollected
        fields = ['id', 'product', 'weight']
        depth = 1
        
class ItemCollectedSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemCollected
        fields = ['id', 'product', 'weight', 'created_by', 'updated_by']
        
        extra_kwargs = {
            'created_by': {'write_only': True},
            'updated_by': {'write_only': True},
        }
        
    def save(self, **kwargs):
        item_collected = super().save()
        pictures = self.context.get("pictures")
        
        if pictures:
            files = [
                ItemCollectedPictures(item_collected=item_collected, picture=file) for file in pictures
            ]
            ItemCollectedPictures.objects.bulk_create(files)
            
        return item_collected
    