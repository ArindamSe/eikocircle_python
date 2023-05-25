from rest_framework import serializers

from repair_shop.models import RepairShop, RepairShopItemPics, RepairShopRecord

class RepairShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepairShop
        fields = ['id', 'name', 'address', 'number', 'city', 'created_by', 'updated_by']
        
        extra_kwargs = {
            'created_by': {'write_only': True},
            'updated_by': {'write_only': True},
        }
        
class RepairShopRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepairShopRecord
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
                RepairShopItemPics(record_item=record, pics=pic) for pic in pictures
            ]
            RepairShopItemPics.objects.bulk_create(files)
            
        return record

class RepairShopItemPicsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepairShopItemPics
        fields = ['id', 'record_item', 'pics']


class RepairShopRecordListSerializer(serializers.ModelSerializer):
    pics = serializers.SerializerMethodField()
    
    def get_pics(self, obj):
        pics_data = RepairShopItemPics.objects.filter(record_item=obj)
        return RepairShopItemPicsSerializer(pics_data, many=True).data
    
    class Meta:
        model = RepairShopRecord
        fields = ['id', 'brand', 'product', 'product_status', 'reusable', 'form', 'discard_item_status', 'price', 'pics']
        depth = 1
        