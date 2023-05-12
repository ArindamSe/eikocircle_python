from django.db.models import Q
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework_tracking.mixins import LoggingMixin

from recycling_center.models import RecyclingCenter, ItemRecycled
from recycling_center.serializers import RecyclingCenterSerializer, ItemRecycledSerializer, ItemRecycledListSerializer

from datetime import datetime, timedelta
class RecyclingCenterViewSet(LoggingMixin, ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = RecyclingCenterSerializer
    
    @staticmethod
    def get_object(pk):
        return get_object_or_404(RecyclingCenter, pk=pk)
    
    @staticmethod
    def get_queryset():
        return RecyclingCenter.objects.all()
    
    def list(self, request, *args, **kwargs):
        data = self.get_queryset()

        response  = {
            'message': 'All Recycling center are listed',
            'data': self.serializer_class(data, many=True).data
        }
        
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
            'created_by': request.user.id,
        }
        
        data = self.serializer_class(data=data)
        data.is_valid(raise_exception=True)
        data.save()
        response = {
            "message": "Successfully created recycling center",
            "data": data.data
        }
        
        return Response(response, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        recyclingcenter = self.get_object(kwargs.pop('pk'))
        
        data = {
            'name': request.data.get('name', recyclingcenter.name),
            'address': request.data.get('address', recyclingcenter.address),
            'number': request.data.get('number', recyclingcenter.number),
            'updated_by': request.user.id,
        }
        
        data = self.serializer_class(data=data, instance=recyclingcenter,)
        data.is_valid(raise_exception=True)
        data.save()
        response =  {
            "message": "Successfully Updated Recycling Center Details",
            "data": data.data,
        }
        
        return Response(response, status=status.HTTP_200_OK)
    
    def partial_update(self, request, *args, **kwargs):
        recyclingcenter = self.get_object(kwargs.pop('pk'))
        
        data = {
            'name': request.data.get('name', recyclingcenter.name),
            'address': request.data.get('address', recyclingcenter.address),
            'number': request.data.get('number', recyclingcenter.number),
            'updated_by': request.user.id,
        }
        
        data = self.serializer_class(data=data, instance=recyclingcenter, partial=True)
        data.is_valid(raise_exception=True)
        data.save()
        response =  {
            "message": "Successfully updated Collection Center Details",
            "data": data.data,
        }
        
        return Response(response, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        id=kwargs.pop('pk')
        recyclingcenter = self.get_object(id)
        ItemRecycled.objects.filter(recyclingcenter__id=id).delete()
        recyclingcenter.delete()
        response = {
            'data': '',
            'message': "Successfully Deleted Recycling Center Details"
        }
        
        return Response(response, status=status.HTTP_204_NO_CONTENT)
    
class ItemRecycledViewSet(LoggingMixin, ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ItemRecycledSerializer
    
    @staticmethod
    def get_object(pk):
        return get_object_or_404(ItemRecycled, pk=pk)
    
    @staticmethod
    def get_queryset():
        return ItemRecycled.objects.all()
    
    def list(self, request, *args, **kwargs):
        product,city,period = request.query_params.get("product"), request.query_params.get('city'), request.query_params.get('period')
        filters = []
        if product:
            filters.append(Q(item_collected__product__name__icontains=product))
        if city:
            filters.append(Q(recyclingcenter__city__icontains=city))
        if period:
            date = datetime.now() - timedelta(days=int(period))
            filters.append(Q(created_at__gte=date))
        
        data = self.get_queryset()
        if product or city or period:
            item = ItemRecycled.objects.filter(*filters)
            data = [obj for obj in item]

        serializer = ItemRecycledListSerializer(data, many=True)
        
        response = []
        
        for i in serializer.data:
            response.append({
                'id': i['id'],
                'reyclingcenter': i['recyclingcenter']['name'],
                'product': i['product']['name'],
                'target': i['target'],
                'recycled': i['recycled'],
            })
        
        return Response(response, status=status.HTTP_200_OK)
    
    def retrieve(self, *args, **kwargs):
        pk = kwargs.pop('pk')
        serializer = ItemRecycledListSerializer(self.get_object(pk))

        response = {
            'id': serializer.data['id'],
            'reyclingcenter': serializer.data['recyclingcenter']['name'],
            'product': serializer.data['product']['name'],
            'target': serializer.data['target'],
            'recycled': serializer.data['recycled'],
        }
        
        return Response(response, status=status.HTTP_200_OK)
    
    def create(self, request):
        data = {
            'recyclingcenter': request.data.get('recyclingcenter'),
            'product': request.data.get('product'),
            'target': request.data.get('target'),
            'recycled': request.data.get('recycled'),
            'created_by': request.user.id,
        }
        
        data = self.serializer_class(data=data)
        data.is_valid(raise_exception=True)
        data.save()
        response = {
            "message": "Successfully created item recycled",
            "data": data.data
        }
        
        return Response(response, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        itemrecycled = self.get_object(kwargs.pop('pk'))
        
        data = {
            'recyclingcenter': request.data.get('recyclingcenter', itemrecycled.recyclingcenter),
            'product': request.data.get('product', itemrecycled.product),
            'target': request.data.get('target', itemrecycled.target),
            'recycled': request.data.get('recycled', itemrecycled.recycled),
            'created_by': request.user.id,
        }
        
        data = self.serializer_class(data=data, instance=itemrecycled,)
        data.is_valid(raise_exception=True)
        data.save()
        response =  {
            "message": "Successfully Updated item recycled Details",
            "data": data.data,
        }
        
        return Response(response, status=status.HTTP_200_OK)
    
    def partial_update(self, request, *args, **kwargs):
        itemrecycled = self.get_object(kwargs.pop('pk'))
        
        data = {
            'recyclingcenter': request.data.get('recyclingcenter', itemrecycled.recyclingcenter),
            'product': request.data.get('product', itemrecycled.product),
            'target': request.data.get('target', itemrecycled.target),
            'recycled': request.data.get('recycled', itemrecycled.recycled),
            'created_by': request.user.id,
        }
        
        data = self.serializer_class(data=data, instance=itemrecycled, partial=True)
        data.is_valid(raise_exception=True)
        data.save()
        response =  {
            "message": "Successfully updated item recycled Details",
            "data": data.data,
        }
        
        return Response(response, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        id=kwargs.pop('pk')
        itemrecycled = self.get_object(id)
        itemrecycled.delete()
        response = {
            'data': '',
            'message': "Successfully Deleted item recycled Details"
        }
        
        return Response(response, status=status.HTTP_204_NO_CONTENT)