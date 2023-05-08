from rest_framework import serializers

from brand_product.models import Brand_product

class BrandProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand_product
        fields = ['id', 'product', 'brand', 'target']
        depth = 2
        
class BrandProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand_product
        fields = ['id', 'product', 'brand', 'target', 'created_by', 'updated_by']
        
        extra_kwargs = {
            'created_by': {'write_only': True},
            'updated_by': {'write_only': True},
        }
    