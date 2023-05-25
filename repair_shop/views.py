from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework_tracking.mixins import LoggingMixin

from repair_shop.models import RepairShop, RepairShopRecord, RepairShopItemPics
from repair_shop.serializers import RepairShopRecordSerializer, RepairShopSerializer, RepairShopRecordListSerializer

class RepairShopViewSet(LoggingMixin, ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = RepairShopSerializer
    
    @staticmethod
    def get_object(pk):
        return get_object_or_404(RepairShop)
    
    @staticmethod
    def get_queryset(self):
        return RepairShop.objects.all()
    
    def list(self, request, *args, **kwargs):
        data =  self.get_queryset()
        serializer = self.serializer_class(data, many=True)
        response = {
            'message': "All Repair shops are listed",
            'data': serializer.data
        }
        
        return Response(response, status=status.HTTP_200_OK)
    
    def retrieve(self, *args, **kwargs):
        pk = kwargs.pop('pk')
        instance = self.get_object(pk)
        serializer = self.serializer_class(instance)
        response = {
            'data': serializer.data
        }
        
        return Response(response, status=status.HTTP_200_OK)
    
    def create(self, request):
        data = {
            'name': request.data.get('name'),
            'address': request.data.get('address'),
            'number': request.data.get('number'),
            'city': request.data.get('city'),
            'created_by': self.request.user.id,
        }
        
        data = self.serializer_class(data=data)
        data.is_valid(raise_exception=True)
        data.save()
        
        response = {
            "message": "Successfully created Repair Shop",
            'data': data,
        }
        
        return Response(response, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object(kwargs.pop('pk'))
        
        data = {
            'name': request.data.get('name', instance.name),
            'address': request.data.get('address', instance.address),
            'number': request.data.get('number', instance.number),
            'city': request.data.get('city', instance.city),
            'updated_by': self.request.user.id,
        }
        
        data = self.serializer_class(data=data, instance=instance)
        data.is_valid(raise_exception=True)
        data.save()

        response = {
            "message": "Successfully updated",
            "data": data.data
        }
        
        return Response(response, status=status.HTTP_200_OK)
        
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object(kwargs.pop('pk'))
        
        data = {
            'name': request.data.get('name', instance.name),
            'address': request.data.get('address', instance.address),
            'number': request.data.get('number', instance.number),
            'city': request.data.get('city', instance.city),
            'updated_by': self.request.user.id,
        }
        
        data = self.serializer_class(data=data, instance=instance, partial=True)
        data.is_valid(raise_exception=True)
        data.save()

        response = {
            "message": "Successfully updated",
            "data": data.data
        }
        
        return Response(response, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        id=kwargs.pop('pk')
        instance = self.get_object(id)
        instance.delete()
        response = {
            'message': "Successfully deleted",
        }
        
        return Response(response, status=status.HTTP_204_NO_CONTENT)