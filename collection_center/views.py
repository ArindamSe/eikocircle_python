from django.db.models import Q
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework_tracking.mixins import LoggingMixin

from collection_center.models import CollectionCenter, CollectedCenterItemCollected
from collection_center.serializers import CollectionCenterSerializer, CollectedCenterItemCollectedSerializer

from datetime import datetime, timedelta

class CollectionCenterViewSet(LoggingMixin, ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CollectionCenterSerializer
    
    @staticmethod
    def get_object(pk):
        return get_object_or_404(CollectionCenter, pk=pk)
    
    @staticmethod
    def get_queryset():
        return CollectionCenter.objects.all()
    
    def list(self, request, *args, **kwargs):
        data = self.get_queryset()
        response = self.serializer_class(data, many=True).data
        return Response(response, status=status.HTTP_200_OK)
    
    def retrieve(self, *args, **kwargs):
        pk = kwargs.pop('pk')
        response = {
            'data': self.serializer_class(self.get_object(pk)).data
        }
        
        return Response(response, status=status.HTTP_200_OK)
    
    def create(self, request):
        data = {
            'name': request.data.get('name'),
            'address': request.data.get('address'),
            'number': request.data.get('number'),
            'medium': request.data.get('medium'),
            'city': request.data.get('city'),
            'created_by': request.user.id,
        }
        
        item_collected =  request.data.get('item_collected', [])
        
        if isinstance(item_collected, str):
            item_collected = [int(item) for item in item_collected.split(',')]
            
        context = {
            'item_collected': item_collected,
        }
        
        data = CollectionCenterSerializer(data=data, context=context)
        data.is_valid(raise_exception=True)
        data.save()
        response = {
            "message": "Successfully created collection center",
            "data": data.data
        }
        
        return Response(response, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        collectioncenter = self.get_object(kwargs.pop('pk'))
        
        data = {
            'name': request.data.get('name', collectioncenter.name),
            'address': request.data.get('address', collectioncenter.address),
            'number': request.data.get('number', collectioncenter.number),
            'medium': request.data.get('medium', collectioncenter.medium),
            'city': request.data.get('city', collectioncenter.city),
            'updated_by': request.user.id,
        }
        
        item_collected =  request.data.get('item_collected', [])
        
        if isinstance(item_collected, str):
            item_collected = [int(item) for item in item_collected.split(',')]
            
        context = {
            'item_collected': item_collected,
        }
        
        data = CollectionCenterSerializer(data=data, instance=collectioncenter, context=context)
        data.is_valid(raise_exception=True)
        data.save()
        response =  {
            "message": "Successfully updated Collection Center Details",
            "data": data.data,
        }
        
        return Response(response, status=status.HTTP_200_OK)
    
    def partial_update(self, request, *args, **kwargs):
        collectioncenter = self.get_object(kwargs.pop('pk'))
        
        data = {
            'name': request.data.get('name', collectioncenter.name),
            'address': request.data.get('address', collectioncenter.address),
            'number': request.data.get('number', collectioncenter.number),
            'medium': request.data.get('medium', collectioncenter.medium),
            'city': request.data.get('city', collectioncenter.city),
            'updated_by': request.user.id,
        }
        
        item_collected =  request.data.get('item_collected', [])
        
        if isinstance(item_collected, str):
            item_collected = [int(item) for item in item_collected.split(',')]
            
        context = {
            'item_collected': item_collected,
        }
        
        data = CollectionCenterSerializer(data=data, instance=collectioncenter, context=context, partial=True)
        data.is_valid(raise_exception=True)
        data.save()
        response =  {
            "message": "Successfully updated Collection Center Details",
            "data": data.data,
        }
        
        return Response(response, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        id=kwargs.pop('pk')
        collectioncenter = self.get_object(id)
        CollectedCenterItemCollected.objects.filter(collection_center__id=id).delete()
        collectioncenter.delete()
        response = {
            'data': '',
            'message': "Successfully deleted Collection Center Details"
        }
        
        return Response(response, status=status.HTTP_204_NO_CONTENT)
    
    
class CollectedCenterItemCollectedViewSet(LoggingMixin, ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CollectedCenterItemCollectedSerializer
    
    @staticmethod
    def get_object(pk):
        return get_object_or_404(CollectedCenterItemCollected, pk=pk)
    
    @staticmethod
    def get_queryset():
        return CollectedCenterItemCollected.objects.all()
    
    def list(self, request, *args, **kwargs):
        product, city, period, brand = request.query_params.get("product"), request.query_params.get('city'), request.query_params.get('period'), request.query_params.get('brand')
        filters = []
        if product:
            filters.append(Q(item_collected__product__name__icontains=product))
        if brand:
            filters.append(Q(item_collected__brand__brand__id=brand))
        if city:
            filters.append(Q(collection_center__city__icontains=city))
        if period:
            date = datetime.now() - timedelta(days=int(period))
            filters.append(Q(created_at__gte=date))
        data = self.get_queryset()
        if product or city or period or brand:
            item = CollectedCenterItemCollected.objects.filter(*filters)
            data = [obj for obj in item]
        data = self.serializer_class(data, many=True).data
        response = []
        for i in data:
            response.append({
                'id': i['id'],
                'collection_center': i['collection_center']['name'],
                'medium': i['collection_center']['medium'],
                'city': i['collection_center']['city'],
                'target': i['item_collected']['target'],
                'collected': i['item_collected']['weight']
            })
        return Response(response, status=status.HTTP_200_OK)
    
    def retrieve(self, *args, **kwargs):
        pk = kwargs.pop('pk')
        data = self.serializer_class(self.get_object(pk)).data
        response = {
            'id': data['id'],
            'collection_center': data['collection_center']['name'],
            'medium': data['collection_center']['medium'],
            'city': data['collection_center']['city'],
            'target': data['item_collected']['target'],
            'collected': data['item_collected']['weight']
        }
        
        return Response(response, status=status.HTTP_200_OK)