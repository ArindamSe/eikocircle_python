from django.db.models import Q
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework_tracking.mixins import LoggingMixin

from collection_center.models import CollectionCenter
from collection_center.serializers import CollectionCenterSerializer
from Item_collected.models import ItemCollected

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
        city = request.query_params.get('city')
        filters = Q()
        
        if city:
            filters &= Q(city__icontains=city)

        queryset = self.get_queryset().filter(filters)
        serializer = self.serializer_class(queryset, many=True)
        response_data = serializer.data
        
        return Response(response_data, status=status.HTTP_200_OK)
    
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
        
        data = CollectionCenterSerializer(data=data)
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
        
        data = CollectionCenterSerializer(data=data, instance=collectioncenter)
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
        
        data = CollectionCenterSerializer(data=data, instance=collectioncenter, partial=True)
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
        ItemCollected.objects.filter(collectioncenter__id=id).delete()
        collectioncenter.delete()
        response = {
            'data': '',
            'message': "Successfully deleted Collection Center Details"
        }
        
        return Response(response, status=status.HTTP_204_NO_CONTENT)
    