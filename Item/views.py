from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework_tracking.mixins import LoggingMixin

from Item.models import Item, ItemMaterialRecoveryReport, ItemProofOfDelivery, ItemRecyclingCertificate, ItemSalePurchaseInvoice
from Item.serializers import ItemSerializer

class ItemViewSet(LoggingMixin, ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ItemSerializer
    
    @staticmethod
    def get_queryset():
        return Item.objects.all()
    
    @staticmethod
    def get_object(pk):
        return get_object_or_404(Item, pk=pk)
    
    def list(self, request, *args, **kwargs):
        data =  self.get_queryset()
        
        response = {
            'status': 'success',
            'data': self.serializer_class(data, many=True).data,
            'message': "item listed successfully"
        }
        
        return Response(response, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        item = self.get_object(pk)
        serializer = ItemSerializer(item)
        response = {
            'status': 'success',
            'data': serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)
    
    def create(self, request):
        data = {
            'item_code': request.data.get('item_code'),
            'target': request.data.get('target'),
            'created_by': request.user.id,
        }
        
        sale = request.FILES.getlist('sale_of_purchase')
        proof = request.FILES.getlist('proof_of_delivery')
        material = request.FILES.getlist('material_recovery_report')
        recycling = request.FILES.getlist('recycling_certificate')
        
        context = {
            'salepurchaseinvoice': sale,
            'proofofdelivery': proof,
            'materialrecoveryreport': material,
            'recyclingcertificate': recycling
        }
        
        data = ItemSerializer(data=data, context=context)
        data.is_valid(raise_exception=True)
        data.save()
        response = {
            "message": f"Successfully created Item",
            "data": data.data
        }
        return Response(response, status=status.HTTP_200_OK)
        
    def update(self, request, *args, **kwargs):
        item = self.get_object(kwargs.pop('pk'))
        data = {
            'item_code': request.data.get('item_code', item.item_code),
            'target': request.data.get('target', item.target),
            'updated_by': request.user.id,
        }
        
        sale = request.FILES.getlist('sale_of_purchase')
        proof = request.FILES.getlist('proof_of_delivery')
        material = request.FILES.getlist('material_recovery_report')
        recycling = request.FILES.getlist('recycling_certificate')
        
        context = {
            'salepurchaseinvoice': sale,
            'proofofdelivery': proof,
            'materialrecoveryreport': material,
            'recyclingcertificate': recycling
        }
        
        data = ItemSerializer(data=data, instance=item, context=context)
        data.is_valid(raise_exception=True)
        data.save()
        response = {
            "message": f"Successfully updated the Item",
            "data": data.data
        }
        return Response(response, status=status.HTTP_201_CREATED)
    
    def partial_update(self, request, *args, **kwargs):
        item = self.get_object(kwargs.pop('pk'))
        data = {
            'item_code': request.data.get('item_code', item.item_code),
            'target': request.data.get('target', item.target),
            'updated_by': request.user.id,
        }
        
        sale = request.FILES.getlist('sale_of_purchase')
        proof = request.FILES.getlist('proof_of_delivery')
        material = request.FILES.getlist('material_recovery_report')
        recycling = request.FILES.getlist('recycling_certificate')
        
        context = {
            'salepurchaseinvoice': sale,
            'proofofdelivery': proof,
            'materialrecoveryreport': material,
            'recyclingcertificate': recycling
        }
        
        data = ItemSerializer(data=data, instance=item, context=context)
        data.is_valid(raise_exception=True)
        data.save()
        response = {
            "message": f"Successfully updated the Item",
            "data": data.data
        }
        return Response(response, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, *args, **kwargs):
        id=kwargs.pop('pk')
        item = self.get_object(id)
        ItemMaterialRecoveryReport.objects.filter(item__id=id).delete()
        ItemProofOfDelivery.objects.filter(item__id=id).delete()
        ItemRecyclingCertificate.objects.filter(item__id=id).delete()
        ItemSalePurchaseInvoice.objects.filter(item__id=id).delete()
        item.delete()
        response= {
            'data': '',
            'message': "Successfully deleted Item"
        }
        return Response(response, status=status.HTTP_204_NO_CONTENT)