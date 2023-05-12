from django.db.models import Q
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework_tracking.mixins import LoggingMixin

from awareness_plan_metrics.models import AwarenessPlanMetrics
from awareness_plan_metrics.serializers import AwarenessPlanMetricsListSerializer, AwarenessPlanMetricsSerializer

class AwarenessPlanMetricsViewSet(LoggingMixin, ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = AwarenessPlanMetricsSerializer
    
    @staticmethod
    def get_object(pk):
        return get_object_or_404(AwarenessPlanMetrics, pk=pk)
    
    @staticmethod
    def get_queryset():
        return AwarenessPlanMetrics.objects.all()
    
    def list(self, request, *args, **kwargs):
        product, city = request.query_params.get("product"), request.query_params.get("city")
        filters = []
        if product:
            filters.append(Q(awarenessplan__product__name__icontains=product))
        if city:
            filters.append(Q(awarenessplan__city__icontains=city))
        data = self.get_queryset()
        if product or city:
            item = AwarenessPlanMetrics.objects.filter(*filters)
            data = [obj for obj in item]
        serializer =  AwarenessPlanMetricsListSerializer(data, many=True).data
        data = []
        response = {
            'message': 'success',
        }
        if serializer:
            response = {
                'theme': serializer[0]['awarenessplan']['theme'],
                'communication': serializer[0]['awarenessplan']['communication'],
                'medium': serializer[0]['awarenessplan']['medium'],
                'city': serializer[0]['awarenessplan']['city'],
                'product': serializer[0]['awarenessplan']['product']['name'],
                'target_audience': serializer[0]['awarenessplan']['target_audience'],
                'brand': serializer[0]['awarenessplan']['brand'],
            }
        for i in serializer:
            data.append({
                'id': i['id'],
                'name': i['name'],
                'proposed': i['proposed'],
                'impacted': i['impacted']
            })
        response['data'] = data
            
        return Response(response, status=status.HTTP_200_OK)
    
    def retrieve(self, *args, **kwargs):
        pk = kwargs.pop('pk')
        response = {
            'data': AwarenessPlanMetricsListSerializer(self.get_object(pk)).data
        }
        
        return Response(response, status=status.HTTP_200_OK)
    
    def create(self, request):
        data = {
            'awarenessplan': request.data.get('awarenessplan'),
            'name': request.data.get('name'),
            'proposed': request.data.get('proposed'),
            'impacted': request.data.get('impacted'),
            'created_by': request.user.id,
        }
        
        data = self.serializer_class(data=data)
        data.is_valid(raise_exception=True)
        data.save()
        
        response = {
            'message': "successfully created metrics plan",
            'data': data.data
        }
        
        return Response(response, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object(kwargs.pop('pk'))
        
        data = {
            'awarenessplan': request.data.get('awarenessplan', instance.awarenessplan),
            'name': request.data.get('name', instance.name),
            'proposed': request.data.get('proposed', instance.proposed),
            'impacted': request.data.get('impacted', instance.impacted),
            'updated_by': request.user.id,
        }
        
        data = self.serializer_class(data=data, instance=instance)
        data.is_valid(raise_exception=True)
        data.save()
        
        response = {
            "message": "successfully updated the metrics details",
            'data': data.data
        }
        
        return Response(response, status=status.HTTP_200_OK)
    
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object(kwargs.pop('pk'))
        
        data = {
            'awarenessplan': request.data.get('awarenessplan', instance.awarenessplan),
            'name': request.data.get('name', instance.name),
            'proposed': request.data.get('proposed', instance.proposed),
            'impacted': request.data.get('impacted', instance.impacted),
            'updated_by': request.user.id,
        }
        
        data = self.serializer_class(data=data, instance=instance, partial=True)
        data.is_valid(raise_exception=True)
        data.save()
        
        response = {
            "message": "successfully updated the metrics details",
            'data': data.data
        }
        
        return Response(response, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        id = kwargs.pop('pk')
        data = self.get_object(id)
        data.delete()
        
        response = {
            "message": "sucessfully delete the data"
        }
        
        return Response(response, status=status.HTTP_204_NO_CONTENT)