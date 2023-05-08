from django.db.models import Q
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework_tracking.mixins import LoggingMixin

from brand_product.models import Brand_product
from brand_product.serializers import BrandProductSerializer, BrandProductListSerializer


class BrandProductViewSet(LoggingMixin, ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = BrandProductSerializer
    
    @staticmethod
    def get_object(pk):
        return get_object_or_404(Brand_product, pk=pk)
    
    @staticmethod
    def get_queryset(brand=None):
        if brand:
            data = Brand_product.objects.filter(brand__name__icontains=brand)
            return data
        return Brand_product.objects.all()
    
    def list(self, request, *args, **kwargs):
        brand = request.query_params.get("brand")
        
        data = self.get_queryset(brand)
        
        serializer = BrandProductListSerializer(data, many=True)
        response = []
        
        for i in serializer.data:
            response.append({
                'id': i['id'],
                'brand': i['brand']['name'],
                'target': i['target'],
                'product': i['product']['name'],
                'item': i['product']['item']['item_code'],
            })

        return Response(response, status=status.HTTP_200_OK)
    
    def retrieve(self, *args, **kwargs):
        pk = kwargs.pop('pk')
        serializer = BrandProductListSerializer(self.get_object(pk)).data
        
        response =  {
                'id': serializer['id'],
                'brand': serializer['brand']['name'],
                'target': serializer['target'],
                'product': serializer['product']['name'],
                'item': serializer['product']['item']['item_code'],
            }
        
        return Response(response, status=status.HTTP_200_OK)
    
    def create(self, request):
        data = {
            'brand': request.data.get('brand'),
            'product': request.data.get('product'),
            'target': request.data.get('target'),
            'created_by': request.user.id,
        }
        
        data = self.serializer_class(data=data)
        data.is_valid(raise_exception=True)
        data.save()
        
        response = {
            "message": "Successfully created your target",
            "data": data.data
        }
        
        return Response(response, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        brandproduct = self.get_object(kwargs.pop('pk'))
        data = {
            'product': request.data.get('product', brandproduct.product),
            'target': request.data.get('target', brandproduct.target),
            'brand': request.data.get('brand', brandproduct.brand),
            'updated_by': request.user.id,
        }
        
        data = self.serializer_class(data=data, instance=brandproduct)
        data.is_valid(raise_exception=True)
        data.save()
        
        response = {
            'message': "Successfully updated your target",
            'data': data.data,
        }
        
        return Response(response, status=status.HTTP_201_CREATED)
        
    def partial_update(self, request, *args, **kwargs):
        brandproduct = self.get_object(kwargs.pop('pk'))
        
        data = {
            'product': request.data.get('product', brandproduct.product),
            'target': request.data.get('target', brandproduct.target),
            'brand': request.data.get('brand', brandproduct.brand),
            'updated_by': request.user.id,
        }
        
        data = self.serializer_class(data=data, instance=brandproduct, partial=True)
        data.is_valid(raise_exception=True)
        data.save()
        
        response = {
            'message': "Successfully updated your target",
            'data': data.data,
        }
        
        return Response(response, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, *args, **kwargs):
        id=kwargs.pop('pk')
        brandproduct = self.get_object(id)
        brandproduct.delete()
        response = {
            'data': '',
            'message': "Successfully deleted your target"
        }
        return Response(response, status=status.HTTP_204_NO_CONTENT)