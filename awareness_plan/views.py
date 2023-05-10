from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework_tracking.mixins import LoggingMixin

from awareness_plan.models import AwarenessPlan, AwarenessPlanPics
from awareness_plan.serializers import AwarenessPlanSerializer, AwarenessPlanListSerializer

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
        data = self.get_queryset()
        
        response = {
            'message': "All plans are listed",
            'data': AwarenessPlanListSerializer(data, many=True).data
        }
        
        return Response(response, status=status.HTTP_200_OK)
    
    def retrieve(self, *args, **kwargs):
        pk = kwargs.pop('pk')
        response = {
            'data': AwarenessPlanListSerializer(self.get_object(pk)).data
        }
        
        return Response(response, status=status.HTTP_200_OK)
    
    def create(self, request):
        data = {
            'product': request.data.get('product'),
            'theme': request.data.get('theme'),
            'medium': request.data.get('medium'),
            'city': request.data.get('city'),
            'communication': request.data.get('communication'),
            'target_audience': request.data.get('target_audience'),
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
            'product': request.data.get('product', instance.product),
            'theme': request.data.get('theme', instance.theme),
            'medium': request.data.get('medium', instance.medium),
            'city': request.data.get('city', instance.city),
            'communication': request.data.get('communication', instance.communication),
            'target_audience': request.data.get('target_audience', instance.target_audience),
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
            'product': request.data.get('product', instance.product),
            'theme': request.data.get('theme', instance.theme),
            'medium': request.data.get('medium', instance.medium),
            'city': request.data.get('city', instance.city),
            'communication': request.data.get('communication', instance.communication),
            'target_audience': request.data.get('target_audience', instance.target_audience),
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