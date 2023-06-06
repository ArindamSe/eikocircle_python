from django.db.models import Q
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework_tracking.mixins import LoggingMixin

from awareness_plan.models import AwarenessPlan, AwarenessPlanPics
from awareness_plan.serializers import AwarenessPlanSerializer, AwarenessPlanListSerializer

from datetime import datetime, timedelta
class AwarenessPlanViewSet(LoggingMixin, ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = AwarenessPlanSerializer
    
    @staticmethod
    def get_object(pk):
        return get_object_or_404(AwarenessPlan, pk=pk)
    
    @staticmethod
    def get_queryset():
        return AwarenessPlan.objects.all()
    
    def list(self, request, *args, **kwargs):
        city, period, brand = request.query_params.get('city'), request.query_params.get('period'), request.query_params.get('brand')
        filters = []
        if city:
            filters.append(Q(city__icontains=city))
        if brand:
            filters.append(Q(brand__id=brand))
        if period:
            date = datetime.now() -  timedelta(days=int(period))
            filters.append(Q(created_at__gte=date))
        data = self.get_queryset()
        if city or brand or period:
            item = AwarenessPlan.objects.filter(*filters)
            data = [obj for obj in item]
        serializer = AwarenessPlanListSerializer(data, many=True).data
        response = []
        
        for i in serializer:
            response.append({
                'id': i['id'],
                'theme': i['theme'],
                'medium': i['medium'],
                'city': i['city'],
                'date': i['date'],
                'price': i['price'],
                'communication': i['communication'],
                'target_audience': i['target_audience'],
                'brand': i['brand'],
                'pics': i['pics'],
                'metrics': i['metrics'],
            })
        
        return Response(response, status=status.HTTP_200_OK)
    
    def retrieve(self, *args, **kwargs):
        pk = kwargs.pop('pk')
        serializer = AwarenessPlanListSerializer(self.get_object(pk)).data
        response = {
                'id': serializer['id'],
                'theme': serializer['theme'],
                'medium': serializer['medium'],
                'city': serializer['city'],
                'date': serializer['date'],
                'price': serializer['price'],
                'communication': serializer['communication'],
                'target_audience': serializer['target_audience'],
                'brand': serializer['brand'],
                'pics': serializer['pics'],
                'metrics': serializer['metrics'],
                'price': serializer['price'],
        }

        return Response(response, status=status.HTTP_200_OK)
    
    def create(self, request):
        data = {
            'theme': request.data.get('theme'),
            'medium': request.data.get('medium'),
            'brand': request.data.get('brand'),
            'city': request.data.get('city'),
            'communication': request.data.get('communication'),
            'target_audience': request.data.get('target_audience'),
            'price': request.data.get['price'],
            'created_by': request.user.id,
        }
        
        pics = request.FILES.getlist('pics')
        
        context = {
            'pics': pics
        }
        
        data = self.serializer_class(data=data, context=context)
        data.is_valid(raise_exception=True)
        data.save()
        
        response = {
            "message": "Successfully created awareness plan",
            'data': data.data
        }
        
        return Response(response, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object(kwargs.pop('pk'))
        
        data = {
            'theme': request.data.get('theme', instance.theme),
            'medium': request.data.get('medium', instance.medium),
            'city': request.data.get('city', instance.city),
            'brand': request.data.get('brand', instance.brand),
            'communication': request.data.get('communication', instance.communication),
            'target_audience': request.data.get('target_audience', instance.target_audience),
            'pics': request.data.get('pics', instance.pics),
            'metrics': request.data.get('metrics', instance.metrics),
            'price': request.data.get('price'),
            'created_by': request.user.id,
        }
        
        pics = request.FILES.getlist('pics')
        
        context = {
            'pics': pics
        }
        
        data = self.serializer_class(data=data, context=context, instance=instance)
        data.is_valid(raise_exception=True)
        data.save()
        
        response = {
            "message": "Successfully updated awareness plan",
            'data': data.data
        }
        
        return Response(response, status=status.HTTP_200_OK)
    
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object(kwargs.pop('pk'))
        
        data = {
            'theme': request.data.get('theme', instance.theme),
            'medium': request.data.get('medium', instance.medium),
            'city': request.data.get('city', instance.city),
            'brand': request.data.get('brand', instance.brand),
            'communication': request.data.get('communication', instance.communication),
            'target_audience': request.data.get('target_audience', instance.target_audience),
            'pics': request.data.get('pics', instance.pics),
            'price': request.data.get('price', instance.price),
            'created_by': request.user.id,
        }
        
        pics = request.FILES.getlist('pics')
        
        context = {
            'pics': pics
        }
        
        data = self.serializer_class(data=data, context=context, instance=instance, partial=True)
        data.is_valid(raise_exception=True)
        data.save()
        
        response = {
            "message": "Successfully updated awareness plan",
            'data': data.data
        }
        
        return Response(response, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        id = kwargs.pop('pk')
        data = self.get_object(id)
        AwarenessPlanPics.objects.filter(awarenessplan__id=id).delete()
        data.delete()
        response = {
            'message': "successfully deleted the awareness plan"
        }
        
        return Response(response, status=status.HTTP_204_NO_CONTENT)
    