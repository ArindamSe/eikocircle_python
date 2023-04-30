from rest_framework import serializers

from product.models import Product

class ProductSerialzerView(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'item', 'name']
        depth = 1
        
class ProductSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'item', 'name', 'created_by', 'updated_by']
        
        extra_kwargs = {
            'created_by': {'write_only': True},
            'updated_by': {'write_only': True},
        }