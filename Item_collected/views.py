from django.db.models import Q
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework_tracking.mixins import LoggingMixin

from Item_collected.models import ItemCollected, ItemCollectedPictures
from Item_collected.serializers import ItemCollectedSerializer, ItemCollectedListSerializer

class ItemCollectedViewSet(LoggingMixin, ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ItemCollectedSerializer
    
    @staticmethod
    def get_object(pk):
        return get_object_or_404(ItemCollected, pk=pk)
    
    @staticmethod
    def get_queryset():
        return ItemCollected.objects.all()
    
    def list(self, request, *args, **kwargs):
        data = self.get_queryset()
        
        response =  {
            'data': ItemCollectedListSerializer(data, many=True).data
        }

        return Response(response, status=status.HTTP_200_OK)
    
    def retrieve(self, *args, **kwargs):
        pk = kwargs.pop('pk')
        response = {
            'data': ItemCollectedListSerializer(self.get_object(pk)).data
        }
        
        return Response(response, status=status.HTTP_200_OK)
    
    def create(self, request):
        data = {
            'collectioncenter': request.data.get('collectioncenter'),
            'product': request.data.get('product'),
            'weight': request.data.get('weight'),
            'brand': request.data.get('brand'),
            'target': request.data.get('target'),
            'created_by': request.user.id,
        }
        
        files = request.FILES.getlist('pictures')
        
        context = {
            'pictures': files,
        }
        
        data = ItemCollectedSerializer(data=data, context=context)
        data.is_valid(raise_exception=True)
        data.save()
        
        response = {
            "message": "Successfully created your collection",
            "data": data.data
        }
        
        return Response(response, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        itemcollected = self.get_object(kwargs.pop('pk'))
        data = {
            'collectioncenter': request.data.get('collectioncenter', itemcollected.collectioncenter),
            'product': request.data.get('product', itemcollected.product),
            'weight': request.data.get('weight', itemcollected.weight),
            'brand': request.data.get('brand', itemcollected.brand),
            'target': request.data.get('target', itemcollected.target),
            'updated_by': request.user.id,
        }
        
        files = request.FILES.getlist("pictures")
        
        context = {
            'pictures': files,
        }
        
        data = ItemCollectedSerializer(data=data, instance=itemcollected, context=context)
        data.is_valid(raise_exception=True)
        data.save()
        
        response = {
            'message': "Successfully updated your collection",
            'data': data.data,
        }
        
        return Response(response, status=status.HTTP_201_CREATED)
        
    def partial_update(self, request, *args, **kwargs):
        itemcollected = self.get_object(kwargs.pop('pk'))
        data = {
            'collectioncenter': request.data.get('collectioncenter', itemcollected.collectioncenter),
            'product': request.data.get('product', itemcollected.product),
            'weight': request.data.get('weight', itemcollected.weight),
            'brand': request.data.get('brand', itemcollected.brand),
            'target': request.data.get('target', itemcollected.target),
            'updated_by': request.user.id,
        }
        
        files = request.FILES.getlist("pictures")
        
        context = {
            'pictures': files,
        }
        
        data = ItemCollectedSerializer(data=data, instance=itemcollected, context=context, partial=True)
        data.is_valid(raise_exception=True)
        data.save()
        
        response = {
            'message': "Successfully updated your collection",
            'data': data.data,
        }
        
        return Response(response, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, *args, **kwargs):
        id=kwargs.pop('pk')
        itemcollected = self.get_object(id)
        ItemCollectedPictures.objects.filter(item_collected__id=id).delete()
        itemcollected.delete()
        response = {
            'data': '',
            'message': "Successfully deleted your collection"
        }
        return Response(response, status=status.HTTP_204_NO_CONTENT)