from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework_tracking.mixins import LoggingMixin

from product.models import Product
from product.serializers import ProductSerialzer, ProductSerialzerView

class ProductViewSet(LoggingMixin, ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerialzer
    
    @staticmethod
    def get_queryset():
        return Product.objects.all()
    
    @staticmethod
    def get_object(pk):
        return get_object_or_404(Product, pk=pk)
    
    def list(self, request, *args, **kwargs):
        data = self.get_queryset()
        
        data = ProductSerialzerView(data, many=True).data
        response = []
        for i in data:
            response.append({
                'id': i['id'],
                'name': i['name'],
                'target': i['item']['target'],
                'item': i['item']["item_code"] })
        
        return Response(response, status=status.HTTP_200_OK)
    
    def retrieve(self, *args, **kwargs):
        pk = kwargs.pop('pk')
        
        response = {
            'data': ProductSerialzerView(self.get_object(pk)).data
        }
        
        return Response(response, status=status.HTTP_200_OK)
    
    def create(self, request):
        data = {
            'item': request.data.get('item'),
            'name': request.data.get('name'),
            'created_by': request.user.id,
        }
        
        data = ProductSerialzer(data=data)
        data.is_valid(raise_exception=True)
        data.save()
        
        response = {
            "message": f"Successfully created Product",
            "data": data.data
        }
        return Response(response, status=status.HTTP_200_OK)
        
    def update(self, request, *args, **kwargs):
        item = self.get_object(kwargs.pop('pk'))
        
        data = {
            'item': request.data.get('item'),
            'name': request.data.get('name'),
            'updated_by': request.user.id,
        }
        
        data = ProductSerialzer(data=data, instance=item)
        data.is_valid(raise_exception=True)
        data.save()
        
        response = {
            "message": f"Successfully updated the Product",
            "data": data.data
        }
        return Response(response, status=status.HTTP_201_CREATED)
    
    def partial_update(self, request, *args, **kwargs):
        item = self.get_object(kwargs.pop('pk'))
        
        data = {
            'item': request.data.get('item'),
            'name': request.data.get('name'),
            'updated_by': request.user.id,
        }
        
        data = ProductSerialzer(data=data, instance=item, partial=True)
        data.is_valid(raise_exception=True)
        data.save()
        
        response = {
            "message": f"Successfully updated the Product",
            "data": data.data
        }
        return Response(response, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, *args, **kwargs):
        id=kwargs.pop('pk')
        item = self.get_object(id)
        item.delete()
        response= {
            'data': '',
            'message': f"Successfully deleted Product name {item_name}"
        }
        return Response(response, status=status.HTTP_204_NO_CONTENT)