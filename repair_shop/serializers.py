from rest_framework import serializers

from repair_shop.models import RepairShop, RepairShopPics
        
class RepairShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepairShop
        fields = ['id', 'brand', 'product', 'product_status', 'reusable', 'form', 'discard_item_status', 'price', 'created_by', 'updated_by']
        
        extra_kwargs = {
            'created_by': {'write_only': True},
            'updated_by': {'write_only': True},
        }
        
    def save(self, **kwargs):
        record = super().save()
        pictures = self.context.get("pictures")
        
        if pictures:
            files = [
                RepairShopPics(shop=record, pics=pic) for pic in pictures
            ]
            RepairShopPics.objects.bulk_create(files)
            
        return record

class RepairShopPicsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepairShopPics
        fields = ['id', 'record_item', 'pics']


class RepairShopListSerializer(serializers.ModelSerializer):
    pics = serializers.SerializerMethodField()
    
    def get_pics(self, obj):
        pics_data = RepairShopPics.objects.filter(record_item=obj)
        return RepairShopPicsSerializer(pics_data, many=True).data
    
    class Meta:
        model = RepairShop
        fields = ['id', 'brand', 'product', 'product_status', 'reusable', 'form', 'discard_item_status', 'price', 'pics']
        depth = 1
        