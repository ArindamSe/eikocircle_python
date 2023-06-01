from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework_tracking.mixins import LoggingMixin

from repair_shop.models import RepairShop, RepairShopPics
from repair_shop.serializers import RepairShopSerializer, RepairShopListSerializer

    
class RepairShopViewSet(LoggingMixin, ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = RepairShopSerializer
    
    @staticmethod
    def get_object(pk):
        return get_object_or_404(RepairShop, pk=pk)
    
    @staticmethod
    def get_queryset():
        return RepairShop.objects.filter()
    
    def list(self, request, *args, **kwargs):
        data = self.get_queryset().filter(created_by=self.request.user.id)
        
        serializer = RepairShopListSerializer(data, many=True).data
        
        response = {
            'data': serializer,
        }
        
        return Response(response, status=status.HTTP_200_OK)
    
    def retrieve(self, *args, **kwargs):
        pk = kwargs.pop('pk')
        instance = self.get_object(pk)
        serializer = RepairShopListSerializer(instance)
        
        response = {
            'data': serializer.data,
        }
        
        return Response(response, status=status.HTTP_200_OK)
    
    def create(self, request):
        data = {
            'brand': request.data.get('brand'),
            'product': request.data.get('product'),
            'product_status': request.data.get('product_status'),
            'reusable': request.data.get('reusable'),
            'form': request.data.get('form'),
            'discard_item_status': request.data.get('discard_item_status'),
            'price': request.data.get('price'),
            'created_by': self.request.user.id,
        }
        
        pictures = request.FILES.getlist('pictures')
        
        context = {
            'pictures': pictures,
        }
        
        data = self.serializer_class(data=data, context=context)
        data.is_valid(raise_exception=True)
        data.save()
        
        response = {
            "message": "Successfully created",
            "data": data.data,
        }
        
        return Response(response, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object(kwargs.pop('pk'))
        
        data = {
            'brand': request.data.get('brand', instance.brand),
            'product': request.data.get('product', instance.product),
            'product_status': request.data.get('product_status', instance.product_status),
            'reusable': request.data.get('reusable', instance.reusable),
            'form': request.data.get('form', instance.form),
            'discard_item_status': request.data.get('discard_item_status', instance.discard_item_status),
            'price': request.data.get('price', instance.price),
            'updated_by': self.request.user.id,
        }
        
        pictures = request.FILES.getlist("pictures")
        
        context = {
            'pictures': pictures,
        }
        
        data = self.serializer_class(data=data, instance=instance, context=context)
        data.is_valid(raise_exception=True)
        data.save()
        
        response = {
            "message": "Successfully updated",
            "data": data.data,
        }
        
        return Response(response, status=status.HTTP_201_CREATED)
    
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object(kwargs.pop('pk'))
        
        data = {
            'brand': request.data.get('brand', instance.brand),
            'product': request.data.get('product', instance.product),
            'product_status': request.data.get('product_status', instance.product_status),
            'reusable': request.data.get('reusable', instance.reusable),
            'form': request.data.get('form', instance.form),
            'discard_item_status': request.data.get('discard_item_status', instance.discard_item_status),
            'price': request.data.get('price', instance.price),
            'updated_by': self.request.user.id,
        }
        
        pictures = request.FILES.getlist("pictures")
        
        context = {
            'pictures': pictures,
        }
        
        data = self.serializer_class(data=data, instance=instance, context=context, partial=True)
        data.is_valid(raise_exception=True)
        data.save()
        
        response = {
            "message": "Successfully updated",
            "data": data.data,
        }
        
        return Response(response, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, *args, **kwargs):
        id=kwargs.pop('pk')
        instance = self.get_object(id)
        RepairShopPics.objects.filter(shop__id=id).delete()
        instance.delete()
        
        response = {
            'message': "Successfully Deleted",
        }
        
        return Response(response, status=status.HTTP_204_NO_CONTENT)
    